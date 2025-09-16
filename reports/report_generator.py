from fpdf import FPDF
import os

class ReportGenerator:
    def __init__(self, metrics: dict, output_file: str = "backtest_report.pdf"):
        self.metrics = metrics
        self.output_file = output_file

    def generate(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Backtest Performance Report", ln=True, align="C")
        pdf.ln(6)

        pdf.set_font("Arial", size=12)
        for k, v in self.metrics.items():
            pdf.cell(0, 8, f"{k}: {v}", ln=True)

        # Save
        dirname = os.path.dirname(self.output_file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        pdf.output(self.output_file)
        print(f"Report written to {self.output_file}")
