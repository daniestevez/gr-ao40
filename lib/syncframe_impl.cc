/* -*- c++ -*- */
/*
 * gr-ao40 GNU Radio OOT module for AO-40 FEC
 *
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "syncframe_impl.h"

#define SYNCLEN 65
#define STEP 80
#define THRESHOLD 0

namespace gr {
  namespace ao40 {

    syncframe::sptr
    syncframe::make()
    {
      return gnuradio::get_initial_sptr
        (new syncframe_impl());
    }

    /*
     * The private constructor
     */
    syncframe_impl::syncframe_impl()
      : gr::sync_block("syncframe",
              gr::io_signature::make(1, 1, sizeof(uint8_t)),
              gr::io_signature::make(0, 0, 0))
    {
      set_history(SYNCLEN * STEP);

      message_port_register_out(pmt::mp("out"));
    }

    /*
     * Our virtual destructor.
     */
    syncframe_impl::~syncframe_impl()
    {
    }

    int
    syncframe_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const uint8_t syncword[SYNCLEN] =
	{1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,0,0,1,0,1,1,0,0,1,0,0,
	 1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,1,1,0,1,1,0,0,0};
      int match;

      const uint8_t *in = (const uint8_t *) input_items[0];

      for (int i = 0; i < noutput_items; i++) {
	match = 0;
	for (int j = 0; j < SYNCLEN; j++) {
	  match += (in[i + j * STEP] & 1) ^ syncword[j];
	}
	if (match >= SYNCLEN - THRESHOLD) {
	  // sync found
	  message_port_pub(pmt::mp("out"),
			   pmt::cons(pmt::PMT_NIL,
				     pmt::init_u8vector(SYNCLEN * STEP, in + i)));
	}
      }

      return noutput_items;
    }

  } /* namespace ao40 */
} /* namespace gr */

