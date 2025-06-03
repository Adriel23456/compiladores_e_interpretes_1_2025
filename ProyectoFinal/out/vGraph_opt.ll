; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@t = local_unnamed_addr global double 0.000000e+00
@x = local_unnamed_addr global double 0.000000e+00
@y = local_unnamed_addr global double 0.000000e+00
@c = local_unnamed_addr global double 0.000000e+00

declare void @vg_set_color(i32) local_unnamed_addr

declare void @vg_draw_pixel(i32, i32) local_unnamed_addr

declare void @vg_clear() local_unnamed_addr

declare void @vg_wait(i32) local_unnamed_addr

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @cos(double) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @sin(double) local_unnamed_addr #0

define i32 @main() local_unnamed_addr {
entry:
  tail call void @vg_clear()
  store double 0.000000e+00, double* @t, align 8
  br label %for.body

for.body:                                         ; preds = %entry, %for.body
  %storemerge3 = phi double [ 0.000000e+00, %entry ], [ %.118, %for.body ]
  %.10 = fmul double %storemerge3, 3.141600e+00
  %.11 = fdiv double %.10, 1.800000e+02
  %.12 = tail call double @cos(double %.11)
  %.13 = fmul double %storemerge3, %.12
  %.14 = fadd double %.13, 3.200000e+02
  store double %.14, double* @x, align 8
  %.16 = load double, double* @t, align 8
  %.18 = fmul double %.16, 3.141600e+00
  %.19 = fdiv double %.18, 1.800000e+02
  %.20 = tail call double @sin(double %.19)
  %.21 = fmul double %.16, %.20
  %.22 = fadd double %.21, 2.400000e+02
  store double %.22, double* @y, align 8
  %.24 = load double, double* @t, align 8
  %.25 = fadd double %.24, 5.000000e-01
  %.26 = fptosi double %.25 to i32
  %.29 = srem i32 %.26, 3
  %.31 = icmp eq i32 %.29, 0
  %.43 = icmp eq i32 %.29, 1
  %. = select i1 %.43, double 2.550000e+02, double 6.528000e+04
  %storemerge2 = select i1 %.31, double 0x416FE00000000000, double %.
  store double %storemerge2, double* @c, align 8
  %.53 = fadd double %storemerge2, 5.000000e-01
  %.54 = fptosi double %.53 to i32
  tail call void @vg_set_color(i32 %.54)
  %.56 = load double, double* @x, align 8
  %.57 = fadd double %.56, 5.000000e-01
  %.58 = fptosi double %.57 to i32
  %.59 = load double, double* @y, align 8
  %.60 = fadd double %.59, 5.000000e-01
  %.61 = fptosi double %.60 to i32
  tail call void @vg_draw_pixel(i32 %.58, i32 %.61)
  %.63 = load double, double* @x, align 8
  %.64 = fadd double %.63, 1.000000e+00
  %.65 = fadd double %.64, 5.000000e-01
  %.66 = fptosi double %.65 to i32
  %.67 = load double, double* @y, align 8
  %.68 = fadd double %.67, 1.000000e+00
  %.69 = fadd double %.68, 5.000000e-01
  %.70 = fptosi double %.69 to i32
  tail call void @vg_draw_pixel(i32 %.66, i32 %.70)
  %.72 = load double, double* @x, align 8
  %.73 = fadd double %.72, 1.000000e+00
  %.74 = fadd double %.73, 5.000000e-01
  %.75 = fptosi double %.74 to i32
  %.76 = load double, double* @y, align 8
  %.77 = fadd double %.76, 5.000000e-01
  %.78 = fptosi double %.77 to i32
  tail call void @vg_draw_pixel(i32 %.75, i32 %.78)
  %.80 = load double, double* @x, align 8
  %.81 = fadd double %.80, 5.000000e-01
  %.82 = fptosi double %.81 to i32
  %.83 = load double, double* @y, align 8
  %.84 = fadd double %.83, 1.000000e+00
  %.85 = fadd double %.84, 5.000000e-01
  %.86 = fptosi double %.85 to i32
  tail call void @vg_draw_pixel(i32 %.82, i32 %.86)
  %.88 = load double, double* @x, align 8
  %.89 = fadd double %.88, -1.000000e+00
  %.90 = fadd double %.89, 5.000000e-01
  %.91 = fptosi double %.90 to i32
  %.92 = load double, double* @y, align 8
  %.93 = fadd double %.92, -1.000000e+00
  %.94 = fadd double %.93, 5.000000e-01
  %.95 = fptosi double %.94 to i32
  tail call void @vg_draw_pixel(i32 %.91, i32 %.95)
  %.97 = load double, double* @x, align 8
  %.98 = fadd double %.97, -1.000000e+00
  %.99 = fadd double %.98, 5.000000e-01
  %.100 = fptosi double %.99 to i32
  %.101 = load double, double* @y, align 8
  %.102 = fadd double %.101, 5.000000e-01
  %.103 = fptosi double %.102 to i32
  tail call void @vg_draw_pixel(i32 %.100, i32 %.103)
  %.105 = load double, double* @x, align 8
  %.106 = fadd double %.105, 5.000000e-01
  %.107 = fptosi double %.106 to i32
  %.108 = load double, double* @y, align 8
  %.109 = fadd double %.108, -1.000000e+00
  %.110 = fadd double %.109, 5.000000e-01
  %.111 = fptosi double %.110 to i32
  tail call void @vg_draw_pixel(i32 %.107, i32 %.111)
  tail call void @vg_wait(i32 100)
  %.117 = load double, double* @t, align 8
  %.118 = fadd double %.117, 5.000000e+00
  store double %.118, double* @t, align 8
  %.6 = fcmp olt double %.118, 3.600000e+02
  br i1 %.6, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  ret i32 0
}

define i32 @_main() local_unnamed_addr {
entry:
  %.2 = tail call i32 @main()
  ret i32 0
}

attributes #0 = { mustprogress nofree nounwind willreturn writeonly }