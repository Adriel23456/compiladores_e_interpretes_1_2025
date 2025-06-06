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
  store double 0x4034000000000000, double* @"r"
  br label %"for.cond.1"
for.incr:
  %".104" = load double, double* @"t"
  %".105" = fadd double %".104", 0x4024000000000000
  store double %".105", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
for.cond.1:
  %".9" = load double, double* @"r"
  %".10" = fcmp olt double %".9", 0x4069000000000000
  br i1 %".10", label %"for.body.1", label %"for.end.1"
for.body.1:
  %".12" = load double, double* @"r"
  %".13" = fadd double %".12", 0x3fe0000000000000
  %".14" = fptosi double %".13" to i32
  %".15" = fadd double 0x4044000000000000, 0x3fe0000000000000
  %".16" = fptosi double %".15" to i32
  %".17" = srem i32 %".14", %".16"
  %".18" = sitofp i32 %".17" to double
  %".19" = fcmp oeq double %".18",              0x0
  br i1 %".19", label %"then", label %"else"
for.incr.1:
  %".40" = load double, double* @"r"
  %".41" = fadd double %".40", 0x4034000000000000
  store double %".41", double* @"r"
  br label %"for.cond.1"
for.end.1:
  store double              0x0, double* @"r"
  br label %"for.cond.2"
then:
  %".21" = sitofp i32 16776960 to double
  store double %".21", double* @"c"
  br label %"endif"
endif:
  %".27" = load double, double* @"c"
  %".28" = fadd double %".27", 0x3fe0000000000000
  %".29" = fptosi double %".28" to i32
  call void @"vg_set_color"(i32 %".29")
  %".31" = fadd double 0x4074000000000000, 0x3fe0000000000000
  %".32" = fptosi double %".31" to i32
  %".33" = fadd double 0x406e000000000000, 0x3fe0000000000000
  %".34" = fptosi double %".33" to i32
  %".35" = load double, double* @"r"
  %".36" = fadd double %".35", 0x3fe0000000000000
  %".37" = fptosi double %".36" to i32
  call void @"vg_draw_circle"(i32 %".32", i32 %".34", i32 %".37")
  br label %"for.incr.1"
else:
  %".24" = sitofp i32 65535 to double
  store double %".24", double* @"c"
  br label %"endif"
for.cond.2:
  %".46" = load double, double* @"r"
  %".47" = fcmp olt double %".46", 0x4069000000000000
  br i1 %".47", label %"for.body.2", label %"for.end.2"
for.body.2:
  %".49" = load double, double* @"r"
  %".50" = load double, double* @"t"
  %".51" = load double, double* @"r"
  %".52" = fadd double %".50", %".51"
  %".53" = fmul double %".52", 0x400921ff2e48e8a7
  %".54" = fdiv double %".53", 0x4066800000000000
  %".55" = call double @"cos"(double %".54")
  %".56" = fmul double %".49", %".55"
  %".57" = fadd double 0x4074000000000000, %".56"
  store double %".57", double* @"x"
  %".59" = load double, double* @"r"
  %".60" = load double, double* @"t"
  %".61" = load double, double* @"r"
  %".62" = fadd double %".60", %".61"
  %".63" = fmul double %".62", 0x400921ff2e48e8a7
  %".64" = fdiv double %".63", 0x4066800000000000
  %".65" = call double @"sin"(double %".64")
  %".66" = fmul double %".59", %".65"
  %".67" = fadd double 0x406e000000000000, %".66"
  store double %".67", double* @"y"
  %".69" = load double, double* @"r"
  %".70" = fadd double %".69", 0x3fe0000000000000
  %".71" = fptosi double %".70" to i32
  %".72" = fadd double 0x403e000000000000, 0x3fe0000000000000
  %".73" = fptosi double %".72" to i32
  %".74" = srem i32 %".71", %".73"
  %".75" = sitofp i32 %".74" to double
  %".76" = fcmp oeq double %".75",              0x0
  br i1 %".76", label %"then.1", label %"else.1"
for.incr.2:
  %".96" = load double, double* @"r"
  %".97" = fadd double %".96", 0x4024000000000000
  store double %".97", double* @"r"
  br label %"for.cond.2"
for.end.2:
  %".100" = fadd double 0x4014000000000000, 0x3fe0000000000000
  %".101" = fptosi double %".100" to i32
  call void @"vg_wait"(i32 %".101")
  br label %"for.incr"
then.1:
  %".78" = sitofp i32 16711935 to double
  store double %".78", double* @"c"
  br label %"endif.1"
endif.1:
  %".84" = load double, double* @"c"
  %".85" = fadd double %".84", 0x3fe0000000000000
  %".86" = fptosi double %".85" to i32
  call void @"vg_set_color"(i32 %".86")
  %".88" = load double, double* @"x"
  %".89" = fadd double %".88", 0x3fe0000000000000
  %".90" = fptosi double %".89" to i32
  %".91" = load double, double* @"y"
  %".92" = fadd double %".91", 0x3fe0000000000000
  %".93" = fptosi double %".92" to i32
  call void @"vg_draw_pixel"(i32 %".90", i32 %".93")
  br label %"for.incr.2"
else.1:
  %".81" = sitofp i32 16777215 to double
  store double %".81", double* @"c"
  br label %"endif.1"
}

@"t" = global double              0x0
@"r" = global double              0x0
@"c" = global double              0x0
@"x" = global double              0x0
@"y" = global double              0x0
define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
