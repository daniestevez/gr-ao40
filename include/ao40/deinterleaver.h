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

#ifndef INCLUDED_AO40_DEINTERLEAVER_H
#define INCLUDED_AO40_DEINTERLEAVER_H

#include <ao40/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ao40 {

    /*!
     * \brief <+description of block+>
     * \ingroup ao40
     *
     */
    class AO40_API deinterleaver : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<deinterleaver> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of ao40::deinterleaver.
       *
       * To avoid accidental use of raw pointers, ao40::deinterleaver's
       * constructor is in a private implementation
       * class. ao40::deinterleaver::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace ao40
} // namespace gr

#endif /* INCLUDED_AO40_DEINTERLEAVER_H */

