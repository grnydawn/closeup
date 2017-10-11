        program main
            implicit none
            integer :: a, b, c

            do a = 1, 3
                do b = 1, 3
                    c = myadd(a, b)
                    print *, a, '+', b, '=', c
                end do
            end do

        contains

            function myadd(d, e) result(f)
                implicit none
                integer, intent(in) :: d, e
                integer :: f

                !scitest$ check d in SB_INTNUM_SET and e in SB_INTNUM_SET

                f = d + e

                !scitest$ set MY_ADD_SET as { n | n == d + e }
                !scitest$ check f in MY_ADD_SET

            end function

        end program
