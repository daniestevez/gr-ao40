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

#ifndef INCLUDED_AO40_SYNCFRAME_IMPL_H
#define INCLUDED_AO40_SYNCFRAME_IMPL_H

#include <ao40/syncframe.h>

#define SYNCLEN 65

namespace gr {
  namespace ao40 {

    class syncframe_impl : public syncframe
    {
     private:
      int d_threshold;
      static const uint8_t d_syncword[SYNCLEN];
            
     public:
      syncframe_impl(int threshold);
      ~syncframe_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace ao40
} // namespace gr

#endif /* INCLUDED_AO40_SYNCFRAME_IMPL_H */

