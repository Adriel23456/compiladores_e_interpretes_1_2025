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
  call void @"vg_clear"()
  store double              0x0, double* @"t"
  br label %"for.cond"
for.cond:
  %".5" = load double, double* @"t"
  %".6" = fcmp olt double %".5", 0x4076800000000000
  br i1 %".6", label %"for.body", label %"for.end"
for.body:
  %".8" = load double, double* @"t"
  %".9" = load double, double* @"t"
  %".10" = fmul double %".9", 0x400921ff2e48e8a7
  %".11" = fdiv double %".10", 0x4066800000000000
  %".12" = call double @"cos"(double %".11")
  %".13" = fmul double %".8", %".12"
  %".14" = fadd double 0x4074000000000000, %".13"
  store double %".14", double* @"x"
  %".16" = load double, double* @"t"
  %".17" = load double, double* @"t"
  %".18" = fmul double %".17", 0x400921ff2e48e8a7
  %".19" = fdiv double %".18", 0x4066800000000000
  %".20" = call double @"sin"(double %".19")
  %".21" = fmul double %".16", %".20"
  %".22" = fadd double 0x406e000000000000, %".21"
  store double %".22", double* @"y"
  %".24" = load double, double* @"t"
  %".25" = fadd double %".24", 0x3fe0000000000000
  %".26" = fptosi double %".25" to i32
  %".27" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".28" = fptosi double %".27" to i32
  %".29" = srem i32 %".26", %".28"
  %".30" = sitofp i32 %".29" to double
  %".31" = fcmp oeq double %".30",              0x0
  br i1 %".31", label %"then", label %"else"
for.incr:
  %".117" = load double, double* @"t"
  %".118" = fadd double %".117", 0x4014000000000000
  store double %".118", double* @"t"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  %".33" = sitofp i32 16711680 to double
  store double %".33", double* @"c"
  br label %"endif"
endif:
  %".52" = load double, double* @"c"
  %".53" = fadd double %".52", 0x3fe0000000000000
  %".54" = fptosi double %".53" to i32
  call void @"vg_set_color"(i32 %".54")
  %".56" = load double, double* @"x"
  %".57" = fadd double %".56", 0x3fe0000000000000
  %".58" = fptosi double %".57" to i32
  %".59" = load double, double* @"y"
  %".60" = fadd double %".59", 0x3fe0000000000000
  %".61" = fptosi double %".60" to i32
  call void @"vg_draw_pixel"(i32 %".58", i32 %".61")
  %".63" = load double, double* @"x"
  %".64" = fadd double %".63", 0x3ff0000000000000
  %".65" = fadd double %".64", 0x3fe0000000000000
  %".66" = fptosi double %".65" to i32
  %".67" = load double, double* @"y"
  %".68" = fadd double %".67", 0x3ff0000000000000
  %".69" = fadd double %".68", 0x3fe0000000000000
  %".70" = fptosi double %".69" to i32
  call void @"vg_draw_pixel"(i32 %".66", i32 %".70")
  %".72" = load double, double* @"x"
  %".73" = fadd double %".72", 0x3ff0000000000000
  %".74" = fadd double %".73", 0x3fe0000000000000
  %".75" = fptosi double %".74" to i32
  %".76" = load double, double* @"y"
  %".77" = fadd double %".76", 0x3fe0000000000000
  %".78" = fptosi double %".77" to i32
  call void @"vg_draw_pixel"(i32 %".75", i32 %".78")
  %".80" = load double, double* @"x"
  %".81" = fadd double %".80", 0x3fe0000000000000
  %".82" = fptosi double %".81" to i32
  %".83" = load double, double* @"y"
  %".84" = fadd double %".83", 0x3ff0000000000000
  %".85" = fadd double %".84", 0x3fe0000000000000
  %".86" = fptosi double %".85" to i32
  call void @"vg_draw_pixel"(i32 %".82", i32 %".86")
  %".88" = load double, double* @"x"
  %".89" = fsub double %".88", 0x3ff0000000000000
  %".90" = fadd double %".89", 0x3fe0000000000000
  %".91" = fptosi double %".90" to i32
  %".92" = load double, double* @"y"
  %".93" = fsub double %".92", 0x3ff0000000000000
  %".94" = fadd double %".93", 0x3fe0000000000000
  %".95" = fptosi double %".94" to i32
  call void @"vg_draw_pixel"(i32 %".91", i32 %".95")
  %".97" = load double, double* @"x"
  %".98" = fsub double %".97", 0x3ff0000000000000
  %".99" = fadd double %".98", 0x3fe0000000000000
  %".100" = fptosi double %".99" to i32
  %".101" = load double, double* @"y"
  %".102" = fadd double %".101", 0x3fe0000000000000
  %".103" = fptosi double %".102" to i32
  call void @"vg_draw_pixel"(i32 %".100", i32 %".103")
  %".105" = load double, double* @"x"
  %".106" = fadd double %".105", 0x3fe0000000000000
  %".107" = fptosi double %".106" to i32
  %".108" = load double, double* @"y"
  %".109" = fsub double %".108", 0x3ff0000000000000
  %".110" = fadd double %".109", 0x3fe0000000000000
  %".111" = fptosi double %".110" to i32
  call void @"vg_draw_pixel"(i32 %".107", i32 %".111")
  %".113" = fadd double 0x4059000000000000, 0x3fe0000000000000
  %".114" = fptosi double %".113" to i32
  call void @"vg_wait"(i32 %".114")
  br label %"for.incr"
else:
  %".36" = load double, double* @"t"
  %".37" = fadd double %".36", 0x3fe0000000000000
  %".38" = fptosi double %".37" to i32
  %".39" = fadd double 0x4008000000000000, 0x3fe0000000000000
  %".40" = fptosi double %".39" to i32
  %".41" = srem i32 %".38", %".40"
  %".42" = sitofp i32 %".41" to double
  %".43" = fcmp oeq double %".42", 0x3ff0000000000000
  br i1 %".43", label %"then.1", label %"else.1"
then.1:
  %".45" = sitofp i32 255 to double
  store double %".45", double* @"c"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  %".48" = sitofp i32 65280 to double
  store double %".48", double* @"c"
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
