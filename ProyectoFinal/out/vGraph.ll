; ModuleID = "vgraph"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"vg_set_color"(i32 %".1")

declare void @"vg_draw_pixel"(i32 %".1", i32 %".2")

declare void @"vg_draw_circle"(i32 %".1", i32 %".2", i32 %".3")

declare void @"vg_draw_line"(i32 %".1", i32 %".2", i32 %".3", i32 %".4")

declare void @"vg_draw_rect"(i32 %".1", i32 %".2", i32 %".3", i32 %".4")

declare void @"vg_clear"()

declare void @"vg_wait"(i32 %".1")

declare double @"cos"(double %".1")

declare double @"sin"(double %".1")

define i32 @"main"()
{
entry:
  store double              0x0, double* @"t"
  br label %"for.cond"
for.cond:
  %".4" = load double, double* @"t"
  %".5" = fcmp olt double %".4", 0x4076800000000000
  br i1 %".5", label %"for.body", label %"for.end"
for.body:
  %".7" = load double, double* @"t"
  %".8" = load double, double* @"t"
  %".9" = fmul double %".8", 0x400921ff2e48e8a7
  %".10" = fdiv double %".9", 0x4066800000000000
  %".11" = call double @"cos"(double %".10")
  %".12" = fmul double %".7", %".11"
  %".13" = fadd double 0x4074000000000000, %".12"
  store double %".13", double* @"x"
  %".15" = load double, double* @"t"
  %".16" = load double, double* @"t"
  %".17" = fmul double %".16", 0x400921ff2e48e8a7
  %".18" = fdiv double %".17", 0x4066800000000000
  %".19" = call double @"sin"(double %".18")
  %".20" = fmul double %".15", %".19"
  %".21" = fadd double 0x406e000000000000, %".20"
  store double %".21", double* @"y"
  %".23" = load double, double* @"t"
  %".24" = fadd double %".23", 0x3fe0000000000000
  %".25" = fptosi double %".24" to i32
  %".26" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".27" = fptosi double %".26" to i32
  %".28" = srem i32 %".25", %".27"
  %".29" = sitofp i32 %".28" to double
  %".30" = fcmp oeq double %".29",              0x0
  br i1 %".30", label %"then", label %"else"
for.incr:
  %".66" = load double, double* @"t"
  %".67" = fadd double %".66", 0x4014000000000000
  store double %".67", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  %".32" = sitofp i32 16711680 to double
  store double %".32", double* @"c"
  br label %"endif"
endif:
  %".51" = load double, double* @"c"
  %".52" = fadd double %".51", 0x3fe0000000000000
  %".53" = fptosi double %".52" to i32
  call void @"vg_set_color"(i32 %".53")
  %".55" = load double, double* @"x"
  %".56" = fadd double %".55", 0x3fe0000000000000
  %".57" = fptosi double %".56" to i32
  %".58" = load double, double* @"y"
  %".59" = fadd double %".58", 0x3fe0000000000000
  %".60" = fptosi double %".59" to i32
  call void @"vg_draw_pixel"(i32 %".57", i32 %".60")
  %".62" = fadd double 0x4049000000000000, 0x3fe0000000000000
  %".63" = fptosi double %".62" to i32
  call void @"vg_wait"(i32 %".63")
  br label %"for.incr"
else:
  %".35" = load double, double* @"t"
  %".36" = fadd double %".35", 0x3fe0000000000000
  %".37" = fptosi double %".36" to i32
  %".38" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".39" = fptosi double %".38" to i32
  %".40" = srem i32 %".37", %".39"
  %".41" = sitofp i32 %".40" to double
  %".42" = fcmp oeq double %".41", 0x3ff0000000000000
  br i1 %".42", label %"then.1", label %"else.1"
then.1:
  %".44" = sitofp i32 255 to double
  store double %".44", double* @"c"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  %".47" = sitofp i32 65280 to double
  store double %".47", double* @"c"
  br label %"endif.1"
}

@"t" = global double              0x0
@"x" = global double              0x0
@"y" = global double              0x0
@"c" = global double              0x0
define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
