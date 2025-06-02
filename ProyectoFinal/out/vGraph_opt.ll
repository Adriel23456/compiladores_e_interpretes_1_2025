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

declare void @vg_wait(i32) local_unnamed_addr

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @cos(double) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn writeonly
declare double @sin(double) local_unnamed_addr #0

define i32 @main() local_unnamed_addr {
entry:
  store double 0.000000e+00, double* @t, align 8
  br label %for.body

for.body:                                         ; preds = %entry, %for.body
  %storemerge3 = phi double [ 0.000000e+00, %entry ], [ %.67, %for.body ]
  %.9 = fmul double %storemerge3, 3.141600e+00
  %.10 = fdiv double %.9, 1.800000e+02
  %.11 = tail call double @cos(double %.10)
  %.12 = fmul double %storemerge3, %.11
  %.13 = fadd double %.12, 3.200000e+02
  store double %.13, double* @x, align 8
  %.15 = load double, double* @t, align 8
  %.17 = fmul double %.15, 3.141600e+00
  %.18 = fdiv double %.17, 1.800000e+02
  %.19 = tail call double @sin(double %.18)
  %.20 = fmul double %.15, %.19
  %.21 = fadd double %.20, 2.400000e+02
  store double %.21, double* @y, align 8
  %.23 = load double, double* @t, align 8
  %.24 = fadd double %.23, 5.000000e-01
  %.25 = fptosi double %.24 to i32
  %.28 = srem i32 %.25, 3
  %.30 = icmp eq i32 %.28, 0
  %.42 = icmp eq i32 %.28, 1
  %. = select i1 %.42, double 2.550000e+02, double 6.528000e+04
  %storemerge2 = select i1 %.30, double 0x416FE00000000000, double %.
  store double %storemerge2, double* @c, align 8
  %.52 = fadd double %storemerge2, 5.000000e-01
  %.53 = fptosi double %.52 to i32
  tail call void @vg_set_color(i32 %.53)
  %.55 = load double, double* @x, align 8
  %.56 = fadd double %.55, 5.000000e-01
  %.57 = fptosi double %.56 to i32
  %.58 = load double, double* @y, align 8
  %.59 = fadd double %.58, 5.000000e-01
  %.60 = fptosi double %.59 to i32
  tail call void @vg_draw_pixel(i32 %.57, i32 %.60)
  tail call void @vg_wait(i32 50)
  %.66 = load double, double* @t, align 8
  %.67 = fadd double %.66, 5.000000e+00
  store double %.67, double* @t, align 8
  %.5 = fcmp olt double %.67, 3.600000e+02
  br i1 %.5, label %for.body, label %for.end

for.end:                                          ; preds = %for.body
  ret i32 0
}

define i32 @_main() local_unnamed_addr {
entry:
  %.2 = tail call i32 @main()
  ret i32 0
}

attributes #0 = { mustprogress nofree nounwind willreturn writeonly }