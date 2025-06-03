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
  %storemerge3 = phi double [ 0.000000e+00, %entry ], [ %.68, %for.body ]
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
  tail call void @vg_wait(i32 125)
  %.67 = load double, double* @t, align 8
  %.68 = fadd double %.67, 5.000000e+00
  store double %.68, double* @t, align 8
  %.6 = fcmp olt double %.68, 3.600000e+02
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