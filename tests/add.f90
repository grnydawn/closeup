      
                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

        program main

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

            implicit none

            integer :: a, b, c


            do a = 1, 3

                do b = 1, 3

                    c = myadd(a, b)

                    print *, a, b, c

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

                end do
                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET
            end do

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

        contains

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET
            function myadd(d, e) result(f)

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET
                implicit none

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET
                integer, intent(in) :: d, e
                integer :: f
     

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET
                f = d + e
                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

            end function
                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET
     
        end program
                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

    

