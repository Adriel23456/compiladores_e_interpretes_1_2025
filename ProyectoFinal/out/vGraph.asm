 .text
 .file "<string>"
 .section .rodata.cst8,"aM",@progbits,8
 .p2align 3
.LCPI0_0:
 .quad 0x400921ff2e48e8a7
.LCPI0_1:
 .quad 0x4066800000000000
.LCPI0_2:
 .quad 0x4074000000000000
.LCPI0_3:
 .quad 0x3fe0000000000000
.LCPI0_4:
 .quad 0x406e000000000000
.LCPI0_6:
 .quad 0x416fe00000000000
.LCPI0_7:
 .quad 0x4014000000000000
.LCPI0_8:
 .quad 0x4076800000000000
 .section .rodata.cst16,"aM",@progbits,16
 .p2align 3
.LCPI0_5:
 .quad 0x40efe00000000000
 .quad 0x406fe00000000000
 .text
 .globl main
 .p2align 4, 0x90
 .type main,@function
main:
 .cfi_startproc
 pushq %rbp
 .cfi_def_cfa_offset 16
 pushq %r15
 .cfi_def_cfa_offset 24
 pushq %r14
 .cfi_def_cfa_offset 32
 pushq %r13
 .cfi_def_cfa_offset 40
 pushq %r12
 .cfi_def_cfa_offset 48
 pushq %rbx
 .cfi_def_cfa_offset 56
 subq $72, %rsp
 .cfi_def_cfa_offset 128
 .cfi_offset %rbx, -56
 .cfi_offset %r12, -48
 .cfi_offset %r13, -40
 .cfi_offset %r14, -32
 .cfi_offset %r15, -24
 .cfi_offset %rbp, -16
 movabsq $t, %rbx
 movq $0, (%rbx)
 xorpd %xmm1, %xmm1
 movabsq $.LCPI0_0, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 24(%rsp)
 movabsq $.LCPI0_1, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 16(%rsp)
 movabsq $.LCPI0_2, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 64(%rsp)
 movabsq $x, %r15
 movabsq $.LCPI0_3, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 8(%rsp)
 movabsq $.LCPI0_4, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 56(%rsp)
 movabsq $y, %r13
 movabsq $.LCPI0_6, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 48(%rsp)
 movabsq $vg_set_color, %r14
 movabsq $vg_draw_pixel, %r12
 movabsq $vg_wait, %rbp
 movabsq $.LCPI0_7, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 40(%rsp)
 movabsq $.LCPI0_8, %rax
 movsd (%rax), %xmm0
 movsd %xmm0, 32(%rsp)
 jmp .LBB0_1
 .p2align 4, 0x90
.LBB0_3:
 movabsq $c, %rax
 movsd %xmm0, (%rax)
 addsd %xmm1, %xmm0
 cvttsd2si %xmm0, %edi
 callq *%r14
 movsd (%r15), %xmm0
 movsd 8(%rsp), %xmm1
 addsd %xmm1, %xmm0
 cvttsd2si %xmm0, %edi
 movsd (%r13), %xmm0
 addsd %xmm1, %xmm0
 cvttsd2si %xmm0, %esi
 callq *%r12
 movl $50, %edi
 callq *%rbp
 movsd (%rbx), %xmm1
 addsd 40(%rsp), %xmm1
 movsd %xmm1, (%rbx)
 movsd 32(%rsp), %xmm0
 ucomisd %xmm1, %xmm0
 jbe .LBB0_4
.LBB0_1:
 movsd %xmm1, (%rsp)
 movapd %xmm1, %xmm0
 mulsd 24(%rsp), %xmm0
 divsd 16(%rsp), %xmm0
 movabsq $cos, %rax
 callq *%rax
 mulsd (%rsp), %xmm0
 addsd 64(%rsp), %xmm0
 movsd %xmm0, (%r15)
 movsd (%rbx), %xmm0
 movsd %xmm0, (%rsp)
 mulsd 24(%rsp), %xmm0
 divsd 16(%rsp), %xmm0
 movabsq $sin, %rax
 callq *%rax
 movsd (%rbx), %xmm1
 movsd 8(%rsp), %xmm2
 addsd %xmm2, %xmm1
 cvttsd2si %xmm1, %eax
 movslq %eax, %rdx
 imulq $1431655766, %rdx, %rax
 movq %rax, %rcx
 shrq $63, %rcx
 shrq $32, %rax
 addl %ecx, %eax
 leal (%rax,%rax,2), %esi
 movl %edx, %ecx
 subl %esi, %ecx
 xorl %eax, %eax
 cmpl $1, %ecx
 sete %cl
 cmpl %esi, %edx
 mulsd (%rsp), %xmm0
 addsd 56(%rsp), %xmm0
 movsd %xmm0, (%r13)
 movsd 48(%rsp), %xmm0
 movapd %xmm2, %xmm1
 je .LBB0_3
 movb %cl, %al
 movabsq $.LCPI0_5, %rcx
 movsd (%rcx,%rax,8), %xmm0
 jmp .LBB0_3
.LBB0_4:
 xorl %eax, %eax
 addq $72, %rsp
 .cfi_def_cfa_offset 56
 popq %rbx
 .cfi_def_cfa_offset 48
 popq %r12
 .cfi_def_cfa_offset 40
 popq %r13
 .cfi_def_cfa_offset 32
 popq %r14
 .cfi_def_cfa_offset 24
 popq %r15
 .cfi_def_cfa_offset 16
 popq %rbp
 .cfi_def_cfa_offset 8
 retq
.Lfunc_end0:
 .size main, .Lfunc_end0-main
 .cfi_endproc

 .globl _main
 .p2align 4, 0x90
 .type _main,@function
_main:
 .cfi_startproc
 pushq %rax
 .cfi_def_cfa_offset 16
 movabsq $main, %rax
 callq *%rax
 xorl %eax, %eax
 popq %rcx
 .cfi_def_cfa_offset 8
 retq
.Lfunc_end1:
 .size _main, .Lfunc_end1-_main
 .cfi_endproc

 .type t,@object
 .bss
 .globl t
 .p2align 3
t:
 .quad 0x0000000000000000
 .size t, 8

 .type x,@object
 .globl x
 .p2align 3
x:
 .quad 0x0000000000000000
 .size x, 8

 .type y,@object
 .globl y
 .p2align 3
y:
 .quad 0x0000000000000000
 .size y, 8

 .type c,@object
 .globl c
 .p2align 3
c:
 .quad 0x0000000000000000
 .size c, 8

 .section ".note.GNU-stack","",@progbits