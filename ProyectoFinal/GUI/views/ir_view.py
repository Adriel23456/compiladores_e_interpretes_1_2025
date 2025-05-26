from __future__ import annotations

import os
import pygame, sys
from GUI.view_base import ViewBase
from GUI.components.button import Button
from GUI.components.horizontal_scrollbar import HorizontalScrollbar
from GUI.components.pop_up_dialog import PopupDialog
from GUI.design_base import design
from config import States, BASE_DIR, CompilerData
from CompilerLogic.intermediateCodeGenerator import IntermediateCodeGenerator
from CompilerLogic.optimizer import Optimizer
from GUI.components.opt_level_dialog import OptLevelDialog

try:
        import pyperclip            # fallback multiplataforma
except ImportError:
    pyperclip = None  

class IRCodeView(ViewBase):

    NOT_FOUND_MSG = ["Error generando IR"]
    _clipboard_ready = False  

      # si no está instalado, no se puede usar

    def setup(self):
        """Requerido por ViewBase; ya está todo hecho en __init__."""
        self._setup_done = True
    def _copy_to_clipboard(self, text: str) -> bool:
        try:
            if pyperclip:
                pyperclip.copy(text)
                return True
            else:
                raise RuntimeError("pyperclip no disponible")
        except Exception as err:
            print("⚠️  pyperclip error:", err)
            self.popup = PopupDialog(self.screen,
                                    "No se pudo copiar al portapapeles",
                                    3000)
            return False


    # ──────────────────────────────────────────
    def __init__(self, view_controller):
        super().__init__(view_controller)
        self.opt_dialog = None          # diálogo de optimización (modal)
        self.last_opt_level = 2         # por defecto


        # Fuente (usa la medium para evitar agregar “code”)
        self.font = design.get_font("medium")
        self.line_h = self.font.get_height() + 4

        # Scroll state
        self.scroll_y = 0
        self.scroll_x = 0
        self.max_scroll_y = 0
        self.scroll_speed = 30  # rueda mouse

        # Scrollbar vertical
        self.scrollbar_rect = None
        self.thumb_rect = None
        self.scrollbar_dragging = False
        self.drag_offset = 0

        # Layout base
        self.margin_side = 25
        self.margin_top = 70
        self.margin_bot = 90
        self.line_number_w = 60    # ancho columna números

        # Cargar IR
        self._load_ir()

        # Crear layout dinámico
        self._rebuild_layout()
        self._recalc_longest_line()
        self.h_scroll = HorizontalScrollbar(self.hbar_rect,
                                            self.max_line_px,
                                            self.code_rect.width)

        # Botones
        self._create_buttons()

    # ──────────────────────────────────────────
    # DATA
    # ──────────────────────────────────────────
    def _load_ir(self):
        # Usa CompilerData.ir_raw si existe; si no, vuelve a generar
        ir_text = getattr(CompilerData, "ir_raw", None) or IntermediateCodeGenerator.generate()
        if ir_text:
            self.ir_lines = ir_text.splitlines()
        else:
            self.ir_lines = self.NOT_FOUND_MSG

    # ──────────────────────────────────────────
    # LAYOUT
    # ──────────────────────────────────────────
    def _rebuild_layout(self):
        full = self.screen.get_rect()
        self.text_rect = pygame.Rect(
            self.margin_side,
            self.margin_top,
            full.width - 2 * self.margin_side,
            full.height - self.margin_top - self.margin_bot - 20  # 20px p/ h-bar
        )
        # código (sin num-línea)
        self.code_rect = pygame.Rect(
            self.text_rect.left + self.line_number_w,
            self.text_rect.top,
            self.text_rect.width - self.line_number_w - 15,  # 15px scrollbar v
            self.text_rect.height,
        )
        # barra horizontal
        self.hbar_rect = pygame.Rect(
            self.text_rect.left,
            self.text_rect.bottom + 4,
            self.text_rect.width,
            16
        )
        # recalcular scroll máximo vertical
        self.max_scroll_y = max(0, len(self.ir_lines) * self.line_h - self.text_rect.height)

    def _create_buttons(self):
        full = self.screen.get_rect()
        btn_w, btn_h, gap = 170, 42, 20
        y_btn = full.bottom - self.margin_bot // 2 - btn_h // 2

        self.back_btn = Button(pygame.Rect(self.margin_side, y_btn, btn_w, btn_h),
                               "Back to Home")
        self.save_btn = Button(pygame.Rect(self.back_btn.rect.right + gap, y_btn, btn_w, btn_h),
                               "Guardar .ll", fixed_width=btn_w)
        self.copy_btn = Button(pygame.Rect(self.save_btn.rect.right + gap, y_btn, btn_w + 20, btn_h),
                               "Copiar", fixed_width=btn_w + 20)
        self.next_btn = Button(pygame.Rect(self.copy_btn.rect.right + gap, y_btn, btn_w + 30, btn_h),
                               "Optimizar IR", fixed_width=btn_w + 30)

    # ──────────────────────────────────────────
    # ANCHO LÍNEA + H-SCROLL
    # ──────────────────────────────────────────
    def _recalc_longest_line(self):
        self.max_line_px = max(self.font.size(ln)[0] + 10 for ln in self.ir_lines) if self.ir_lines else 0
        if hasattr(self, "h_scroll"):
            self.h_scroll.update_content_width(self.max_line_px)

    # ──────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────
    def _ir_valido(self) -> bool:
        return self.ir_lines and not self.ir_lines[0].startswith("Error")

    def _run_optimizer(self, level: int):
        """Ejecuta Optimizer y devuelve (ok, mensaje)."""
        ir_source = "\n".join(self.ir_lines)

        optimized = Optimizer.optimize(
            ir_source,
            output_path=None,
            opt_level=level
        )

        if optimized is None:
            return False, "optimización falló (ver consola)"
        else:
            CompilerData.ir_optimized = optimized  # ← 🧠 Esta línea FALTABA
            return True, ""



    # ──────────────────────────────────────────
    # EVENTS
    # ──────────────────────────────────────────
    def handle_events(self, events):
        for ev in events:
            # Botones
            if self.back_btn.handle_event(ev):
                self.view_controller.change_state(States.EDITOR)

            elif self.save_btn.handle_event(ev):
                if self._ir_valido():
                    path = os.path.join(BASE_DIR, "out", "vGraph.ll")
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write('\n'.join(self.ir_lines))
                    print(f"IR guardado en {path}")

            elif self.copy_btn.handle_event(ev):
                if self._ir_valido():
                    self._copy_to_clipboard('\n'.join(self.ir_lines))

            elif self.next_btn.handle_event(ev):
                # abrir diálogo modal para elegir el nivel
                self.opt_dialog = OptLevelDialog(self.screen)

            # ─ diálogo de selección de nivel ─
            if self.opt_dialog:
                self.opt_dialog.handle_events(events)
                if self.opt_dialog.selected is not None:
                    level = self.opt_dialog.selected
                    self.last_opt_level = level
                    ir_text = '\n'.join(self.ir_lines)
                    ok, msg = self._run_optimizer(level)
                    self.opt_dialog = None
                    if ok:
                        self.view_controller.change_state(States.IR_OPTIMIZED)
                    else:
                        self.popup = PopupDialog(self.screen,
                            f"Optimización O{level} falló:\n{msg}", 4000)


            # Scroll vertical rueda
            if ev.type == pygame.MOUSEWHEEL:
                if self.text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = max(0, min(self.max_scroll_y,
                                               self.scroll_y - ev.y * self.scroll_speed))

            # Drag scrollbar vertical
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.thumb_rect and self.thumb_rect.collidepoint(ev.pos):
                    self.scrollbar_dragging = True
                    self.drag_offset = ev.pos[1] - self.thumb_rect.y
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.scrollbar_dragging = False
            if ev.type == pygame.MOUSEMOTION and self.scrollbar_dragging:
                new_y = ev.pos[1] - self.drag_offset
                track_h = self.scrollbar_rect.height - self.thumb_rect.height
                ratio = max(0, min(1, (new_y - self.scrollbar_rect.y) / track_h))
                self.scroll_y = int(ratio * self.max_scroll_y)

            # H-scrollbar (horizontal)
            self.h_scroll.handle_event(ev)

        # actualizar desplazamiento horizontal
        self.scroll_x = self.h_scroll.get_scroll_offset()

    # ──────────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────────
    def update(self, dt):
        pass

    # ──────────────────────────────────────────
    # RENDER
    # ──────────────────────────────────────────
    def _draw_vscrollbar(self):
        bar_w = 10
        self.scrollbar_rect = pygame.Rect(self.text_rect.right - bar_w,
                                          self.text_rect.top,
                                          bar_w,
                                          self.text_rect.height)
        pygame.draw.rect(self.screen, design.colors["button"], self.scrollbar_rect)

        # Thumb
        ratio_visible = self.text_rect.height / (self.text_rect.height + self.max_scroll_y)
        thumb_h = max(20, int(self.scrollbar_rect.height * ratio_visible))
        track_h = self.scrollbar_rect.height - thumb_h
        thumb_y = self.scrollbar_rect.y + int(track_h * (self.scroll_y / max(1, self.max_scroll_y)))
        self.thumb_rect = pygame.Rect(self.scrollbar_rect.x, thumb_y, bar_w, thumb_h)
        pygame.draw.rect(self.screen, design.colors["button_hover"], self.thumb_rect, 0, 3)

    def render(self):
        self.screen.fill(design.colors["background"])

        # Título
        title = design.get_font("large").render("Intermediate Representation (LLVM IR)",
                                                True, design.colors["text"])
        self.screen.blit(title, title.get_rect(midtop=(self.screen_rect.centerx, 20)))

        # Marco y fondo
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_rect)
        pygame.draw.rect(self.screen, design.colors["textbox_border"], self.text_rect, 2)

        # Clip
        clip = self.screen.subsurface(self.text_rect)
        clip.fill((255, 255, 255))

        # Zona números de línea
        ln_bg = pygame.Rect(0, 0, self.line_number_w - 5, self.text_rect.height)
        pygame.draw.rect(clip, (240, 240, 240), ln_bg)
        pygame.draw.line(clip, (200, 200, 200),
                        (self.line_number_w - 5, 0), (self.line_number_w - 5, self.text_rect.height))

        # Dibujar líneas visibles
        first_idx = int(self.scroll_y / self.line_h)
        last_idx = min(len(self.ir_lines),
                    first_idx + self.text_rect.height // self.line_h + 2)
        y = -self.scroll_y % self.line_h
        for i in range(first_idx, last_idx):
            ln_surf = self.font.render(f"{i + 1:4d}", True, (100, 100, 100))
            clip.blit(ln_surf, (5, y))
            code_surf = self.font.render(self.ir_lines[i], True, (0, 0, 0))
            clip.blit(code_surf, (self.line_number_w, y))
            y += self.line_h

        # Scrollbars
        if self.max_scroll_y > 0:
            self._draw_vscrollbar()
        self.h_scroll.render(self.screen)

        # Botones principales
        self.back_btn.render(self.screen)
        self.save_btn.render(self.screen)
        self.copy_btn.render(self.screen)
        self.next_btn.render(self.screen)

        # Diálogo modal de optimización
        if self.opt_dialog:
            self.opt_dialog.render()

        # Popup (si existe)
        if hasattr(self, "popup") and self.popup:
            if self.popup.render():
                self.popup = None


    # ──────────────────────────────────────────
    # RESIZE (llámalo en VIDEORESIZE)
    # ──────────────────────────────────────────
    def resize(self, new_size):
        self._rebuild_layout()
        self._recalc_longest_line()
        self.h_scroll.rect = self.hbar_rect
        self.h_scroll.update_content_width(self.max_line_px)
