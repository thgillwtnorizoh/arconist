using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Arconist.Records;

// ENGINEERING JSON backend, not original SQLite bytes/migrations/durability proof.
// One process owns an exclusive lock for this instance. Corruption, incompatible
// schema, external edits or I/O failure block writes until an explicit reopen.
public sealed class LocalRecordStore:IDisposable
{
    private sealed record Document(int SchemaVersion,List<ChartRecord> Records);
    public const int SchemaVersion=1;
    public const int MaxBytes=4*1024*1024;
    private static readonly JsonSerializerOptions JsonOptions=new(){PropertyNamingPolicy=JsonNamingPolicy.CamelCase,WriteIndented=true,RespectRequiredConstructorParameters=true,UnmappedMemberHandling=JsonUnmappedMemberHandling.Disallow};
    private Dictionary<string,ChartRecord> records=new(StringComparer.Ordinal);
    private FileStream? ownership;
    private string? fingerprint;
    private bool disposed;
    public string FilePath {get;}
    public string BackupPath=>FilePath+".previous";
    public bool HasError {get;private set;}
    public string Detail {get;private set;}="Ready";
    public bool LoadedFromDisk {get;private set;}
    public int WriteAttempts {get;private set;}
    public int SuccessfulWrites {get;private set;}
    public int Count=>records.Count;
    private static string Hash(byte[] bytes)=>Convert.ToHexString(SHA256.HashData(bytes));
    private void Block(Exception e){HasError=true;Detail="Records unavailable: "+e.Message+" Original file preserved. Close the app and back up the file before manual recovery. Path: "+FilePath;}
    public LocalRecordStore(string path)
    {
        FilePath=Path.GetFullPath(path);
        try
        {
            Directory.CreateDirectory(Path.GetDirectoryName(FilePath)!);
            ownership=new FileStream(FilePath+".lock",FileMode.OpenOrCreate,FileAccess.ReadWrite,FileShare.None);
            if(!File.Exists(FilePath))return;
            byte[] bytes=ReadBounded();
            var document=JsonSerializer.Deserialize<Document>(bytes,JsonOptions)??throw new InvalidDataException("Empty record document.");
            if(document.SchemaVersion!=SchemaVersion||document.Records==null||document.Records.Count>4096)throw new InvalidDataException("Unsupported record schema or excessive record count.");
            var loaded=new Dictionary<string,ChartRecord>(StringComparer.Ordinal);
            foreach(var row in document.Records)
            {
                if(row==null||row.Identity==null||row.BestScore==null)throw new InvalidDataException("Missing record fields.");
                row.Identity.Validate();row.BestScore.Validate();
                if(!loaded.TryAdd(row.Identity.Key,row))throw new InvalidDataException("Duplicate record identity.");
            }
            records=loaded;fingerprint=Hash(bytes);LoadedFromDisk=true;Detail="Loaded saved records";
        }
        catch(Exception e) when(e is IOException or InvalidDataException or UnauthorizedAccessException or JsonException or NotSupportedException or ArgumentException){Block(e);}
    }
    private byte[] ReadBounded()
    {
        using var stream=new FileStream(FilePath,FileMode.Open,FileAccess.Read,FileShare.Read);
        if(stream.Length>MaxBytes)throw new InvalidDataException("Record file exceeds supported size.");
        using var buffer=new MemoryStream();stream.CopyTo(buffer);
        if(buffer.Length>MaxBytes)throw new InvalidDataException("Record file grew beyond supported size.");
        return buffer.ToArray();
    }
    public ChartRecord? Get(ChartIdentity identity)=>records.TryGetValue(identity.Key,out var record)?record:null;
    public RecordOutcome Record(ChartIdentity identity,SavedResult result)
    {
        WriteAttempts++;
        if(disposed||HasError)return new(identity.Key,false,false,false,false,"ERROR",disposed?"Record store closed":Detail);
        string? temporary=null;bool created=false;
        try
        {
            identity.Validate();result.Validate();
            // Detect cooperating or external changes instead of overwriting bytes
            // that this instance did not successfully load or itself commit.
            if(File.Exists(FilePath)?fingerprint==null||Hash(ReadBounded())!=fingerprint:fingerprint!=null)
                throw new IOException("Record file changed or disappeared while open.");
            var old=Get(identity);
            bool score=RecordRules.ImprovesScore(result.Score,old?.BestScore.Score);
            bool clear=RecordRules.ImprovesClear(result.Category,old?.ClearType??-1);
            if(!score&&!clear)return new(identity.Key,true,false,false,false,"UNCHANGED","Saved best unchanged");
            var updated=new Dictionary<string,ChartRecord>(records,StringComparer.Ordinal);
            updated[identity.Key]=new ChartRecord(identity,score?result:old!.BestScore,clear?result.Category:old!.ClearType);
            if(updated.Count>4096)throw new IOException("Record store reached its supported identity capacity.");
            byte[] bytes=JsonSerializer.SerializeToUtf8Bytes(new Document(SchemaVersion,updated.OrderBy(p=>p.Key,StringComparer.Ordinal).Select(p=>p.Value).ToList()),JsonOptions);
            if(bytes.Length>MaxBytes)throw new IOException("Record store reached its supported size.");
            temporary=FilePath+".tmp-"+Guid.NewGuid().ToString("N");
            using(var stream=new FileStream(temporary,FileMode.CreateNew,FileAccess.Write,FileShare.None))
            {created=true;stream.Write(bytes);stream.Flush(flushToDisk:true);}
            if(File.Exists(FilePath))File.Replace(temporary,FilePath,BackupPath);else File.Move(temporary,FilePath);
            records=updated;fingerprint=Hash(bytes);SuccessfulWrites++;Detail="Saved records";
            return new(identity.Key,true,true,score,clear,score&&clear?"SCORE_AND_CLEAR":score?"SCORE":"CLEAR",score&&clear?"Saved best score and clear":score?"Saved better score":"Saved stronger clear");
        }
        catch(Exception e) when(e is IOException or InvalidDataException or UnauthorizedAccessException or JsonException or NotSupportedException or ArgumentException)
        {Block(e);return new(identity.Key,false,false,false,false,"ERROR",Detail);}
        finally
        {
            if(created&&temporary!=null)try{if(File.Exists(temporary))File.Delete(temporary);}catch(IOException){}catch(UnauthorizedAccessException){}
        }
    }
    public void Dispose(){if(disposed)return;disposed=true;ownership?.Dispose();ownership=null;}
}
