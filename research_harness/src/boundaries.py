"""ELF virtual addresses, not host or allocated emulator object addresses."""
PC_SKIPS = [
    ['0xf72110', '0xf72158', 'Platform GLView attachment'],
    ['0x16a4238', '0x16a48d8', 'Shutter panels replaced with native Node proxies'],
    ['0x121581c', '0x121584c', 'Loading overlay omitted'],
    ['0xa507c4', '0xa519ec', 'Loading artwork prefix; native Node target supplied'],
    ['0xa51adc', '0xa5213c', 'Remaining information artwork and canary omitted'],
    ['0x196fdac', '0x196ffac', 'Information child closing visuals omitted'],
    ['0x891190', '0x89164c', 'Results UI prefix; application/scratch registers restored'],
    ['0x891688', '0x89219c', 'Middle results UI omitted; native save branch retained'],
    ['0x8921dc', '0x8928e0', 'Post-save progression/UI omitted'],
]
