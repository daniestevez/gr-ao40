# gr-ao40
GNU Radio OOT module for AO-40 FEC

This is a FEC decoder for the [AO-40 FEC format](http://www.ka9q.net/papers/ao40tlm.html),
which is used in the FUNcube satellites.

## Installation

This module includes a hierarchical block in
`examples/ao40_fec_decoder.grc`. You need to install it by opening it with
`gnuradio-companion` and hitting the "Generate" button (next to the "Play"
button).

## Requirements

 * [libfec](https://github.com/daniestevez/libfec)
 * The CCSDS descrambler hierarchical block from
   [gr-satellites](https://github.com/daniestevez/gr-satellites)
 