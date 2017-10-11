PROG := add.f90
FC := gfortran

build:
	${FC} -o add.exe ${PROG}

run: build
	./add.exe

clean:
	rm -f add.exe *.o *.mod
