using Arconist.Core;
namespace Arconist.Records;
public sealed record ChartRegistration(string Id,string File,ChartProfile Profile,string PackagedSha256)
{
    public ChartIdentity Identity(string aff)=>ChartIdentity.FromAff(Id,Profile,aff);
}
public static class BundledCatalog
{
    public static IReadOnlyList<ChartRegistration> Entries {get;}=Array.AsReadOnly(new[]{
        new ChartRegistration("widen_lanes_practice","widen_lanes_practice.aff",ChartProfile.S01Mixed,"fbba9f6e5c119414226a67c764bb4d3b7e54a5f82afb10dd8f137e3acdf721b8"),
        new ChartRegistration("widen_camera_practice","widen_camera_practice.aff",ChartProfile.S01Mixed,"bbe432212a10d68e7ce334c90f84c899318804dd1dfa61e1b4a9f189b6623c89"),
        new ChartRegistration("native_widen_control","native_widen_control.aff",ChartProfile.S01Mixed,"ed24ad498f97fdee73258c5d1ba8cf2e37e9934237196221818b8b02b9eb0ec5"),
        new ChartRegistration("native_widen_camera","native_widen_camera.aff",ChartProfile.S01Mixed,"78554144eafca66fd45c3aa054d2976cb923376cf1210da2ea28b14ee2059093"),
        new ChartRegistration("native_widen_lanes","native_widen_lanes.aff",ChartProfile.S01Mixed,"d8e6cfd800d0d8697854f28d5add18e2eaa9a85ebd432f3ba9eb33b604dd5a28"),
        new ChartRegistration("s01_mixed","s01_mixed.aff",ChartProfile.S01Mixed,"bab0a2563e52e9ba4c6dd4a74d959ef9c372db83d499a7b8964aa190da602a3c"),
        new ChartRegistration("s01_crossing","s01_crossing.aff",ChartProfile.S01Mixed,"4dec8cf11aeb1d1aed7710a524fa7ac13ce00e66208c93e956915cb58acc03ce"),
        new ChartRegistration("s01_grouped","s01_grouped.aff",ChartProfile.S01Mixed,"98328136d19f8e36e173060926aceef9dffa87e81fa166c3dc1e138fcc2b0be3"),
        new ChartRegistration("grouped_practice","grouped_practice.aff",ChartProfile.R010,"767f65e85414b3dbcab2b8d7ffd864f2dc61ee69a0b613529a41fef7a3ec5646"),
        new ChartRegistration("native_timing_group","native_timing_group.aff",ChartProfile.R010,"e2427ac5e68232e0be335518fac60d3e362aab9131437319ffab8b9cf143a8b6"),
        new ChartRegistration("native_reverse_scroll","native_reverse_scroll.aff",ChartProfile.R010,"bcba5d21f8f00ebece3c0f212ccbf5f10b95e20c2daa9e635b083d9deb84e32b"),
        new ChartRegistration("native_noinput_group","native_noinput_group.aff",ChartProfile.R010,"fe4d8247e5017ad0388b06731cdd0723a73a58c6749e131d11989a1bc215a4d3"),
        new ChartRegistration("linked_practice","linked_practice.aff",ChartProfile.R010,"1e307bcc32643f20830ab78a505f34937156cc64d2bc10997e28d28631c6576f"),
        new ChartRegistration("native_linked_arc_successors","native_linked_arc_successors.aff",ChartProfile.R010,"c0abe4ca157ea34888c27571081383284df5b7ca61e58cce3815ac41ecedd527"),
        new ChartRegistration("arctap_practice","arctap_practice.aff",ChartProfile.R010,"9271ffd88179c30c36340fd55992af866daf3d6a2641d94aaa23b086129c849f"),
        new ChartRegistration("native_arc_tap","native_arc_tap.aff",ChartProfile.R010,"b7ec1c7fd945c2dca5c1a6151c07137c302531505cd299b7df5ae94256f3d0ff"),
        new ChartRegistration("sky_practice","sky_practice.aff",ChartProfile.R010,"9e6d2f3ee69d54324a7dbacaeb735ed418f58a17682f0ea61af70bdc6704d163"),
        new ChartRegistration("native_moving_arc","native_moving_arc.aff",ChartProfile.R010,"8f47dda5f94f3f553709be131c9f0470f4bf89e9faf34e14f215dd6195a084cc"),
        new ChartRegistration("audible_practice","audible_practice.aff",ChartProfile.R010,"4d287015e9aad7b160ef230f31bd46b75dca5791c84eb559b98e604d3bb3d3d8"),
        new ChartRegistration("audible_aff120","audible_aff120.aff",ChartProfile.R010,"647649223d78c782208139c5781179b2cb8b59ac8e9478df284eec19b5f2d697"),
        new ChartRegistration("mixed_practice","mixed_practice.aff",ChartProfile.R010,"d7e0736507e85d50e29a0e9b4bebfa638f8291b7cbffff7d2f47d61f1c1e4b11"),
        new ChartRegistration("practice","practice.aff",ChartProfile.R010,"9808162c888cff297b22422b4560974bcbba4c68eef8fb4038810413d4dbdade"),
        new ChartRegistration("ordinary_two_tap","ordinary_two_tap.aff",ChartProfile.R010,"5cb2fbd1e9e5646b89f72f1b85b9315852db394ef1bb12bf0ee38ad97c44d026"),
        new ChartRegistration("native_hold","native_hold.aff",ChartProfile.R010,"603c78c37c228436bf47e37d0826aa8b2efa0d5c93177b3fefbfb253379cee6e"),
        new ChartRegistration("hold_first","hold_first.aff",ChartProfile.R010,"32e3d87fe3a547d66b3f5c1f8e6f1abd06d4097a9708f166de8f6d101a2e3539"),
        new ChartRegistration("tap_first","tap_first.aff",ChartProfile.R010,"2be8778065223f9ea6170beed1250dbe9b7201f079294e44203b38ec12e55fc1"),
    });
    public static ChartRegistration Find(string file)=>Entries.SingleOrDefault(c=>c.File==file)??throw new NotSupportedException("Records support only the26bundled chart identities.");
}
