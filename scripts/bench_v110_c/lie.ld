
SECTIONS {
  . = 0x400000;
  .text : { *(.text*) *(.rodata*) }
  /DISCARD/ : { *(.comment) *(.note*) }
}
