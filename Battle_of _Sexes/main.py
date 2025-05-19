# main.py
from visualizations import draw_game_tree, draw_normal_form_game
from analysis import calculate_game_analysis
from outputs import write_story_txt, write_analysis_txt, write_latex_document, compile_latex_to_pdf

def main():
    """Generates all outputs: story, analysis, visualizations, and LaTeX document."""
    write_story_txt()
    draw_game_tree()
    draw_normal_form_game()
    analysis = calculate_game_analysis()
    write_analysis_txt(analysis)
    write_latex_document(analysis)
    compile_latex_to_pdf()
if __name__ == "__main__":
    main()