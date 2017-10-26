        program main
            implicit none
            integer :: a, b, c
            do a = 1, 3
                do b = 1, 3
                    c = myadd(a, b)
                    print *, a, b, c
                end do
            end do
        contains
            function myadd(d, e) result(f)
                implicit none
                integer, intent(in) :: d, e
                integer :: f
                f = d + e
            end function
        end program
