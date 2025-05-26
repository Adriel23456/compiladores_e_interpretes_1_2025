"""
Views package initialization file
"""
from GUI.views.editor_view import EditorView
from GUI.views.config_view import ConfigView
from GUI.views.credits_view import CreditsView
from GUI.views.grammar_view import GrammarView
from GUI.views.lexical_analysis_view import LexicalAnalysisView
from GUI.views.syntactic_analysis_view import SyntacticAnalysisView
from GUI.views.symbol_table_view import SymbolTableView
from GUI.views.ir_view import IRCodeView
from GUI.views.optimizer_view import OptimizerView

__all__ = ['EditorView', 'ConfigView', 'CreditsView', 'GrammarView', 'LexicalAnalysisView', 'SyntacticAnalysisView', 'SymbolTableView','IRCodeView','OptimizerView']