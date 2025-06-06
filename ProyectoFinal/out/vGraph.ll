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
  call void @"vg_set_color"(i32 0)
  %".3" = fadd double              0x0, 0x3fe0000000000000
  %".4" = fptosi double %".3" to i32
  %".5" = fadd double              0x0, 0x3fe0000000000000
  %".6" = fptosi double %".5" to i32
  %".7" = fadd double 0x4088f80000000000, 0x3fe0000000000000
  %".8" = fptosi double %".7" to i32
  %".9" = fadd double 0x4082b80000000000, 0x3fe0000000000000
  %".10" = fptosi double %".9" to i32
  call void @"vg_draw_rect"(i32 %".4", i32 %".6", i32 %".8", i32 %".10")
  store double 0x4014000000000000, double* @"depth"
  store double 0x4099000000000000, double* @"len100"
  store double              0x0, double* @"pos"
  br label %"for.cond"
for.cond:
  %".16" = load double, double* @"pos"
  %".17" = fcmp olt double %".16", 0x4018000000000000
  br i1 %".17", label %"for.body", label %"for.end"
for.body:
  %".19" = load double, double* @"pos"
  %".20" = fcmp oeq double %".19",              0x0
  br i1 %".20", label %"then", label %"else"
for.incr:
  %".76" = load double, double* @"pos"
  %".77" = fadd double %".76", 0x3ff0000000000000
  store double %".77", double* @"pos"
  br label %"for.cond"
for.end:
  ret i32 0
then:
  store double 0x4062c00000000000, double* @"x1"
  store double 0x4062c00000000000, double* @"y1"
  br label %"endif"
endif:
  store double              0x0, double* @"axis"
  br label %"for.cond.1"
else:
  %".25" = load double, double* @"pos"
  %".26" = fcmp oeq double %".25", 0x3ff0000000000000
  br i1 %".26", label %"then.1", label %"else.1"
then.1:
  store double 0x4084500000000000, double* @"x1"
  store double 0x4062c00000000000, double* @"y1"
  br label %"endif.1"
endif.1:
  br label %"endif"
else.1:
  %".31" = load double, double* @"pos"
  %".32" = fcmp oeq double %".31", 0x4000000000000000
  br i1 %".32", label %"then.2", label %"else.2"
then.2:
  store double 0x4079000000000000, double* @"x1"
  store double 0x4059000000000000, double* @"y1"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.2:
  %".37" = load double, double* @"pos"
  %".38" = fcmp oeq double %".37", 0x4008000000000000
  br i1 %".38", label %"then.3", label %"else.3"
then.3:
  store double 0x4062c00000000000, double* @"x1"
  store double 0x407c200000000000, double* @"y1"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
else.3:
  %".43" = load double, double* @"pos"
  %".44" = fcmp oeq double %".43", 0x4010000000000000
  br i1 %".44", label %"then.4", label %"else.4"
then.4:
  store double 0x4084500000000000, double* @"x1"
  store double 0x407c200000000000, double* @"y1"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
else.4:
  store double 0x4079000000000000, double* @"x1"
  store double 0x407f400000000000, double* @"y1"
  br label %"endif.4"
for.cond.1:
  %".58" = load double, double* @"axis"
  %".59" = fcmp olt double %".58", 0x4018000000000000
  br i1 %".59", label %"for.body.1", label %"for.end.1"
for.body.1:
  %".61" = load double, double* @"axis"
  %".62" = fmul double %".61", 0x404e000000000000
  store double %".62", double* @"ang"
  %".64" = load double, double* @"x1"
  %".65" = load double, double* @"y1"
  %".66" = load double, double* @"len100"
  %".67" = load double, double* @"ang"
  %".68" = load double, double* @"depth"
  call void @"triBranch"(double %".64", double %".65", double %".66", double %".67", double %".68")
  br label %"for.incr.1"
for.incr.1:
  %".71" = load double, double* @"axis"
  %".72" = fadd double %".71", 0x3ff0000000000000
  store double %".72", double* @"axis"
  br label %"for.cond.1"
for.end.1:
  br label %"for.incr"
}

define void @"triBranch"(double %".1", double %".2", double %".3", double %".4", double %".5")
{
entry:
  %"x1" = alloca double
  store double %".1", double* %"x1"
  %"y1" = alloca double
  store double %".2", double* %"y1"
  %"len100" = alloca double
  store double %".3", double* %"len100"
  %"ang" = alloca double
  store double %".4", double* %"ang"
  %"depth" = alloca double
  store double %".5", double* %"depth"
  %".12" = load double, double* %"depth"
  %".13" = fcmp oeq double %".12",              0x0
  %"x2" = alloca double
  %"y2" = alloca double
  %"col" = alloca double
  br i1 %".13", label %"then", label %"endif"
then:
  call void @"vg_set_color"(i32 65280)
  %".16" = load double, double* %"x1"
  %".17" = fadd double %".16", 0x3fe0000000000000
  %".18" = fptosi double %".17" to i32
  %".19" = load double, double* %"y1"
  %".20" = fadd double %".19", 0x3fe0000000000000
  %".21" = fptosi double %".20" to i32
  %".22" = fadd double 0x4000000000000000, 0x3fe0000000000000
  %".23" = fptosi double %".22" to i32
  call void @"vg_draw_circle"(i32 %".18", i32 %".21", i32 %".23")
  ret void
endif:
  %".26" = load double, double* %"x1"
  %".27" = load double, double* %"len100"
  %".28" = load double, double* %"ang"
  %".29" = fmul double %".28", 0x400921ff2e48e8a7
  %".30" = fdiv double %".29", 0x4066800000000000
  %".31" = call double @"cos"(double %".30")
  %".32" = fmul double %".27", %".31"
  %".33" = fdiv double %".32", 0x4059000000000000
  %".34" = fadd double %".26", %".33"
  store double %".34", double* %"x2"
  %".36" = load double, double* %"y1"
  %".37" = load double, double* %"len100"
  %".38" = load double, double* %"ang"
  %".39" = fmul double %".38", 0x400921ff2e48e8a7
  %".40" = fdiv double %".39", 0x4066800000000000
  %".41" = call double @"sin"(double %".40")
  %".42" = fmul double %".37", %".41"
  %".43" = fdiv double %".42", 0x4059000000000000
  %".44" = fsub double %".36", %".43"
  store double %".44", double* %"y2"
  %".46" = load double, double* %"depth"
  %".47" = fadd double %".46", 0x3fe0000000000000
  %".48" = fptosi double %".47" to i32
  %".49" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".50" = fptosi double %".49" to i32
  %".51" = srem i32 %".48", %".50"
  %".52" = sitofp i32 %".51" to double
  %".53" = fcmp oeq double %".52",              0x0
  br i1 %".53", label %"then.1", label %"else"
then.1:
  %".55" = sitofp i32 16711680 to double
  store double %".55", double* %"col"
  br label %"endif.1"
endif.1:
  %".113" = load double, double* %"col"
  %".114" = fadd double %".113", 0x3fe0000000000000
  %".115" = fptosi double %".114" to i32
  call void @"vg_set_color"(i32 %".115")
  %".117" = load double, double* %"x1"
  %".118" = fadd double %".117", 0x3fe0000000000000
  %".119" = fptosi double %".118" to i32
  %".120" = load double, double* %"y1"
  %".121" = fadd double %".120", 0x3fe0000000000000
  %".122" = fptosi double %".121" to i32
  %".123" = load double, double* %"x2"
  %".124" = fadd double %".123", 0x3fe0000000000000
  %".125" = fptosi double %".124" to i32
  %".126" = load double, double* %"y2"
  %".127" = fadd double %".126", 0x3fe0000000000000
  %".128" = fptosi double %".127" to i32
  call void @"vg_draw_line"(i32 %".119", i32 %".122", i32 %".125", i32 %".128")
  %".130" = load double, double* %"x1"
  %".131" = fadd double %".130", 0x3ff0000000000000
  %".132" = fadd double %".131", 0x3fe0000000000000
  %".133" = fptosi double %".132" to i32
  %".134" = load double, double* %"y1"
  %".135" = fadd double %".134", 0x3fe0000000000000
  %".136" = fptosi double %".135" to i32
  %".137" = load double, double* %"x2"
  %".138" = fadd double %".137", 0x3ff0000000000000
  %".139" = fadd double %".138", 0x3fe0000000000000
  %".140" = fptosi double %".139" to i32
  %".141" = load double, double* %"y2"
  %".142" = fadd double %".141", 0x3fe0000000000000
  %".143" = fptosi double %".142" to i32
  call void @"vg_draw_line"(i32 %".133", i32 %".136", i32 %".140", i32 %".143")
  %".145" = load double, double* %"len100"
  %".146" = fmul double %".145", 0x4049000000000000
  %".147" = fdiv double %".146", 0x4059000000000000
  store double %".147", double* %"len100"
  %".149" = load double, double* %"x2"
  %".150" = load double, double* %"y2"
  %".151" = load double, double* %"len100"
  %".152" = load double, double* %"ang"
  %".153" = load double, double* %"depth"
  %".154" = fsub double %".153", 0x3ff0000000000000
  call void @"triBranch"(double %".149", double %".150", double %".151", double %".152", double %".154")
  %".156" = load double, double* %"x2"
  %".157" = load double, double* %"y2"
  %".158" = load double, double* %"len100"
  %".159" = load double, double* %"ang"
  %".160" = fsub double %".159", 0x404e000000000000
  %".161" = load double, double* %"depth"
  %".162" = fsub double %".161", 0x3ff0000000000000
  call void @"triBranch"(double %".156", double %".157", double %".158", double %".160", double %".162")
  %".164" = load double, double* %"x2"
  %".165" = load double, double* %"y2"
  %".166" = load double, double* %"len100"
  %".167" = load double, double* %"ang"
  %".168" = fadd double %".167", 0x404e000000000000
  %".169" = load double, double* %"depth"
  %".170" = fsub double %".169", 0x3ff0000000000000
  call void @"triBranch"(double %".164", double %".165", double %".166", double %".168", double %".170")
  ret void
else:
  %".58" = load double, double* %"depth"
  %".59" = fadd double %".58", 0x3fe0000000000000
  %".60" = fptosi double %".59" to i32
  %".61" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".62" = fptosi double %".61" to i32
  %".63" = srem i32 %".60", %".62"
  %".64" = sitofp i32 %".63" to double
  %".65" = fcmp oeq double %".64", 0x3ff0000000000000
  br i1 %".65", label %"then.2", label %"else.1"
then.2:
  %".67" = sitofp i32 16776960 to double
  store double %".67", double* %"col"
  br label %"endif.2"
endif.2:
  br label %"endif.1"
else.1:
  %".70" = load double, double* %"depth"
  %".71" = fadd double %".70", 0x3fe0000000000000
  %".72" = fptosi double %".71" to i32
  %".73" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".74" = fptosi double %".73" to i32
  %".75" = srem i32 %".72", %".74"
  %".76" = sitofp i32 %".75" to double
  %".77" = fcmp oeq double %".76", 0x4000000000000000
  br i1 %".77", label %"then.3", label %"else.2"
then.3:
  %".79" = sitofp i32 65280 to double
  store double %".79", double* %"col"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
else.2:
  %".82" = load double, double* %"depth"
  %".83" = fadd double %".82", 0x3fe0000000000000
  %".84" = fptosi double %".83" to i32
  %".85" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".86" = fptosi double %".85" to i32
  %".87" = srem i32 %".84", %".86"
  %".88" = sitofp i32 %".87" to double
  %".89" = fcmp oeq double %".88", 0x4008000000000000
  br i1 %".89", label %"then.4", label %"else.3"
then.4:
  %".91" = sitofp i32 65535 to double
  store double %".91", double* %"col"
  br label %"endif.4"
endif.4:
  br label %"endif.3"
else.3:
  %".94" = load double, double* %"depth"
  %".95" = fadd double %".94", 0x3fe0000000000000
  %".96" = fptosi double %".95" to i32
  %".97" = fadd double 0x4018000000000000, 0x3fe0000000000000
  %".98" = fptosi double %".97" to i32
  %".99" = srem i32 %".96", %".98"
  %".100" = sitofp i32 %".99" to double
  %".101" = fcmp oeq double %".100", 0x4010000000000000
  br i1 %".101", label %"then.5", label %"else.4"
then.5:
  %".103" = sitofp i32 255 to double
  store double %".103", double* %"col"
  br label %"endif.5"
endif.5:
  br label %"endif.4"
else.4:
  %".106" = sitofp i32 16711935 to double
  store double %".106", double* %"col"
  br label %"endif.5"
}

@"depth" = global double              0x0
@"len100" = global double              0x0
@"pos" = global double              0x0
@"x1" = global double              0x0
@"y1" = global double              0x0
@"axis" = global double              0x0
@"ang" = global double              0x0
define i32 @"_main"()
{
entry:
  %".2" = call i32 @"main"()
  ret i32 %".2"
}
