# GUI/views/optimizer_view.py
from __future__ import annotations

import os
import pygame
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.components.horizontal_scrollbar import HorizontalScrollbar
from GUI.components.pop_up_dialog import PopupDialog
from GUI.design_base import design
from config import States, BASE_DIR, CompilerData

try:
    import pyperclip
except ImportError:
    pyperclip = None


class OptimizerView(ViewBase):
    """
    Muestra el IR optimizado guardado en out/vGraph_opt.ll.
    Permite copiar/guardar y volver al IR “sin optimizar”.
    """

    NOT_FOUND_MSG = ["Error, no se encontró vGraph_opt.ll — ejecuta la optimización primero."]

    # ---------------------------------------------------------------------
    def __init__(self, view_controller):
        super().__init__(view_controller)

        self.font = design.get_font("medium")
        self.line_h = self.font.get_height() + 4

        # estado scroll
        self.scroll_y = 0
        self.scroll_x = 0
        self.max_scroll_y = 0
        self.scroll_speed = 30

        # layout base
        self.margin_side = 25
        self.margin_top = 70
        self.margin_bot = 90
        self.line_number_w = 60

        # cargar IR optimizado
        self._load_ir()

        # layout dinámico
        self._rebuild_layout()
        self._recalc_longest_line()
        self.h_scroll = HorizontalScrollbar(self.hbar_rect,
                                            self.max_line_px,
                                            self.code_rect.width)

        # botones
        self._create_buttons()

    # ---------------------------------------------------------------------
    # Cargar fichero
    def _load_ir(self):
        # Usa CompilerData.ir_optimized si lo hubieras guardado;
        # si no, lee el archivo generado por Optimizer.optimize
        ir_text = getattr(CompilerData, "ir_optimized", None)
        if ir_text is None:
            opt_path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
            if os.path.exists(opt_path):
                with open(opt_path, "r", encoding="utf-8") as fh:
                    ir_text = fh.read()
        self.ir_lines = ir_text.splitlines() if ir_text else self.NOT_FOUND_MSG

    # ---------------------------------------------------------------------
    # Layout helpers
    def _rebuild_layout(self):
        full = self.screen.get_rect()
        self.text_rect = pygame.Rect(
            self.margin_side,
            self.margin_top,
            full.width - 2 * self.margin_side,
            full.height - self.margin_top - self.margin_bot - 20
        )
        self.code_rect = pygame.Rect(
            self.text_rect.left + self.line_number_w,
            self.text_rect.top,
            self.text_rect.width - self.line_number_w - 15,
            self.text_rect.height
        )
        self.hbar_rect = pygame.Rect(
            self.text_rect.left,
            self.text_rect.bottom + 4,
            self.text_rect.width,
            16
        )
        self.max_scroll_y = max(0, len(self.ir_lines) * self.line_h - self.text_rect.height)

    def _recalc_longest_line(self):
        self.max_line_px = max(self.font.size(ln)[0] + 10 for ln in self.ir_lines) if self.ir_lines else 0
        if hasattr(self, "h_scroll"):
            self.h_scroll.update_content_width(self.max_line_px)

    def _create_buttons(self):
        full = self.screen.get_rect()
        btn_w, btn_h, gap = 170, 42, 20
        y_btn = full.bottom - self.margin_bot // 2 - btn_h // 2

        self.back_btn = Button(pygame.Rect(self.margin_side, y_btn, btn_w, btn_h),
                               "IR sin optimizar")
        self.save_btn = Button(pygame.Rect(self.back_btn.rect.right + gap, y_btn, btn_w, btn_h),
                               "Guardar .ll", fixed_width=btn_w)
        self.copy_btn = Button(pygame.Rect(self.save_btn.rect.right + gap, y_btn, btn_w + 20, btn_h),
                               "Copiar", fixed_width=btn_w + 20)
        self.next_btn = Button(pygame.Rect(self.copy_btn.rect.right + gap, y_btn,
                                    btn_w, btn_h),
                        "Next ▸", fixed_width=btn_w)

    # ---------------------------------------------------------------------
    # Utilidades
    def _ir_valido(self) -> bool:
        return self.ir_lines and not self.ir_lines[0].startswith("Error")

    def _copy_to_clipboard(self, text: str):
        try:
            if pyperclip:
                pyperclip.copy(text)
                return True
        except Exception as err:
            print("clipboard error:", err)
        self.popup = PopupDialog(self.screen, "No se pudo copiar", 3000)
        return False

    # ---------------------------------------------------------------------
    # Eventos
    def handle_events(self, events):
        for ev in events:
            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.IR_CODE_VIEW)

            elif self.save_btn.handle_event(ev):
                if self._ir_valido():
                    path = os.path.join(BASE_DIR, "out", "vGraph_opt.ll")
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write('\n'.join(self.ir_lines))
                    print(f"IR optimizado guardado en {path}")

            elif self.copy_btn.handle_event(ev):
                if self._ir_valido():
                    self._copy_to_clipboard('\n'.join(self.ir_lines))
            elif self.next_btn.handle_event(ev):
                # Aquí eliges el estado que represente la siguiente fase.
                # Ejemplo ficticio:
                self.view_controller.change_state(States.CODEGEN_VIEW)

            # scroll ratón
            if ev.type == pygame.MOUSEWHEEL:
                if self.text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = max(0, min(self.max_scroll_y,
                                               self.scroll_y - ev.y * self.scroll_speed))
            # h-scrollbar
            self.h_scroll.handle_event(ev)

        self.scroll_x = self.h_scroll.get_scroll_offset()

    # ---------------------------------------------------------------------
    # Render
    def _draw_vscrollbar(self):
        bar_w = 10
        sb_rect = pygame.Rect(self.text_rect.right - bar_w,
                              self.text_rect.top,
                              bar_w,
                              self.text_rect.height)
        pygame.draw.rect(self.screen, design.colors["button"], sb_rect)

        ratio_visible = self.text_rect.height / (self.text_rect.height + self.max_scroll_y)
        thumb_h = max(20, int(sb_rect.height * ratio_visible))
        track_h = sb_rect.height - thumb_h
        thumb_y = sb_rect.y + int(track_h * (self.scroll_y / max(1, self.max_scroll_y)))
        pygame.draw.rect(self.screen, design.colors["button_hover"],
                         (sb_rect.x, thumb_y, bar_w, thumb_h), border_radius=3)

    def render(self):
        self.screen.fill(design.colors["background"])

        # título
        title = design.get_font("large").render("LLVM IR optimizado", True, design.colors["text"])
        self.screen.blit(title, title.get_rect(midtop=(self.screen_rect.centerx, 20)))

        # área texto
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.text_rect, 2)

        clip = self.screen.subsurface(self.text_rect)
        clip.fill((255, 255, 255))

        # números de línea
        ln_bg = pygame.Rect(0, 0, self.line_number_w - 5, self.text_rect.height)
        pygame.draw.rect(clip, (240, 240, 240), ln_bg)
        pygame.draw.line(clip, (200, 200, 200),
                         (self.line_number_w - 5, 0), (self.line_number_w - 5, self.text_rect.height))

        first = int(self.scroll_y / self.line_h)
        last = min(len(self.ir_lines), first + self.text_rect.height // self.line_h + 2)
        y = -self.scroll_y % self.line_h
        for i in range(first, last):
            ln_surf = self.font.render(f"{i + 1:4d}", True, (100, 100, 100))
            clip.blit(ln_surf, (5, y))
            txt_surf = self.font.render(self.ir_lines[i], True, (0, 0, 0))
            clip.blit(txt_surf, (self.line_number_w, y))
            y += self.line_h

        if self.max_scroll_y > 0:
            self._draw_vscrollbar()
        self.h_scroll.render(self.screen)

        # botones
        self.back_btn.render(self.screen)
        self.save_btn.render(self.screen)
        self.copy_btn.render(self.screen)
        self.next_btn.render(self.screen)

        # popup
        if hasattr(self, "popup") and self.popup:
            if self.popup.render():
                self.popup = None

    # ---------------------------------------------------------------------
    def resize(self, new_size):
        self._rebuild_layout()
        self._recalc_longest_line()
        self.h_scroll.rect = self.hbar_rect
        self.h_scroll.update_content_width(self.max_line_px)
    def setup(self):
        """No necesita inicialización adicional: marcaremos como hecho."""
        self._setup_done = True
        # -----------------------------------------------------------------
    def update(self, dt: float):
        """No hay lógica de actualización frame-a-frame para esta vista."""
        pass

