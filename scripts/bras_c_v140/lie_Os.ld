
SECTIONS {
  . = 0x1400000;
  .text : { *(.text*) }
  .rodata : { *(.rodata*) }
  .data : { *(.data*) }
  /DISCARD/ : { *(.comment) *(.note*) }
}
