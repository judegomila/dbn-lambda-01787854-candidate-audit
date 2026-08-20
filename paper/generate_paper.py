#!/usr/bin/env python3
"""Generate the deterministic referee manuscript for the 0.1787854 candidate."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "pdf" / "dbn_lambda_01787854_candidate_audit.pdf"
RELEASE_DATE = "27 July 2026"
REPOSITORY_URL = (
    "https://github.com/judegomila/dbn-lambda-01787854-candidate-audit"
)

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#176B87")
TEAL = colors.HexColor("#147D70")
GOLD = colors.HexColor("#C58B24")
RED = colors.HexColor("#A33A32")
INK = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#52606D")
LIGHT_BLUE = colors.HexColor("#EAF3F8")
LIGHT_TEAL = colors.HexColor("#E7F5F1")
LIGHT_GOLD = colors.HexColor("#FBF3E0")
LIGHT_RED = colors.HexColor("#F9EAE8")
LIGHT_GRAY = colors.HexColor("#F2F4F6")
LINE = colors.HexColor("#C7D0D9")
WHITE = colors.white


class ReleaseCanvas(canvas.Canvas):
    """Deterministic PDF metadata and byte-stable creation dates."""

    def __init__(self, *args, **kwargs):
        kwargs["invariant"] = 1
        super().__init__(*args, **kwargs)
        self.setTitle(
            "A Candidate for an Unconditional Computer-Assisted Proof "
            "of Lambda <= 0.1787854"
        )
        self.setAuthor("Jude Gomila")
        self.setSubject("Referee manuscript and reproducibility record")
        self.setCreator("ReportLab; source paper/generate_paper.py")
        self.setKeywords(
            "de Bruijn-Newman constant, computer-assisted proof, "
            "interval arithmetic, external review"
        )


class CandidateDocTemplate(BaseDocTemplate):
    """Single-column letter manuscript with bookmarks and a generated TOC."""

    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="body",
        )
        self.addPageTemplates(
            [PageTemplate(id="release", frames=[frame], onPage=draw_page)]
        )
        self._bookmark_index = 0

    def beforeDocument(self):
        self._bookmark_index = 0

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        if flowable.style.name not in {"H1", "H2"}:
            return
        level = 0 if flowable.style.name == "H1" else 1
        text = flowable.getPlainText()
        key = f"section-{self._bookmark_index}"
        self._bookmark_index += 1
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=False)
        self.notify("TOCEntry", (level, text, self.page, key))


def draw_page(canv: canvas.Canvas, doc: BaseDocTemplate) -> None:
    """Draw the running header and footer after the cover."""

    page = canv.getPageNumber()
    if page == 1:
        return
    width, height = LETTER
    canv.saveState()
    canv.setStrokeColor(LINE)
    canv.setLineWidth(0.45)
    canv.line(
        doc.leftMargin,
        height - 0.47 * inch,
        width - doc.rightMargin,
        height - 0.47 * inch,
    )
    canv.setFillColor(MUTED)
    canv.setFont("Helvetica", 7.35)
    canv.drawString(
        doc.leftMargin,
        height - 0.36 * inch,
        "LAMBDA 0.1787854 - CANDIDATE REVIEW",
    )
    canv.drawRightString(
        width - doc.rightMargin, height - 0.36 * inch, RELEASE_DATE
    )
    canv.line(
        doc.leftMargin,
        0.49 * inch,
        width - doc.rightMargin,
        0.49 * inch,
    )
    canv.drawString(
        doc.leftMargin,
        0.34 * inch,
        "Candidate for an unconditional proof - not independently validated",
    )
    canv.drawRightString(
        width - doc.rightMargin, 0.34 * inch, f"Page {page}"
    )
    canv.restoreState()


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=29,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11.7,
            leading=16.5,
            textColor=MUTED,
            spaceAfter=15,
        ),
        "CoverResult": ParagraphStyle(
            "CoverResult",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "CoverMeta": ParagraphStyle(
            "CoverMeta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=13.5,
            textColor=MUTED,
        ),
        "H1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17.5,
            leading=21,
            textColor=NAVY,
            spaceBefore=0,
            spaceAfter=9,
            keepWithNext=True,
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.4,
            leading=14.6,
            textColor=BLUE,
            spaceBefore=9,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=9.25,
            leading=13.0,
            textColor=INK,
            spaceAfter=6.5,
            allowWidows=0,
            allowOrphans=0,
        ),
        "BodySmall": ParagraphStyle(
            "BodySmall",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=8.15,
            leading=11.1,
            textColor=INK,
            spaceAfter=5,
        ),
        "Lead": ParagraphStyle(
            "Lead",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10.45,
            leading=14.8,
            textColor=INK,
            spaceAfter=9,
        ),
        "Callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.55,
            leading=12.1,
            textColor=INK,
        ),
        "CalloutStrong": ParagraphStyle(
            "CalloutStrong",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.15,
            leading=12.7,
            textColor=NAVY,
        ),
        "Equation": ParagraphStyle(
            "Equation",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.9,
            leading=11.0,
            textColor=NAVY,
            leftIndent=7,
            rightIndent=7,
        ),
        "Code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.05,
            leading=9.7,
            textColor=INK,
        ),
        "Caption": ParagraphStyle(
            "Caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=7.25,
            leading=9.7,
            textColor=MUTED,
            spaceBefore=3,
            spaceAfter=7,
        ),
        "TableHead": ParagraphStyle(
            "TableHead",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.25,
            leading=9.0,
            textColor=WHITE,
        ),
        "TableBody": ParagraphStyle(
            "TableBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.05,
            leading=9.1,
            textColor=INK,
        ),
        "TableBodySmall": ParagraphStyle(
            "TableBodySmall",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.45,
            leading=8.2,
            textColor=INK,
        ),
        "Bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=9.05,
            leading=12.6,
            leftIndent=14,
            firstLineIndent=-8,
            bulletIndent=3,
            textColor=INK,
            spaceAfter=3.5,
        ),
        "TOC0": ParagraphStyle(
            "TOC0",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=12.5,
            leftIndent=0,
            firstLineIndent=0,
            textColor=NAVY,
            spaceBefore=3,
        ),
        "TOC1": ParagraphStyle(
            "TOC1",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.0,
            leading=10.7,
            leftIndent=14,
            firstLineIndent=0,
            textColor=MUTED,
        ),
        "Reference": ParagraphStyle(
            "Reference",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=8.1,
            leading=11.0,
            leftIndent=15,
            firstLineIndent=-15,
            textColor=INK,
            spaceAfter=6,
        ),
    }


STYLES = make_styles()


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def h1(text: str) -> Paragraph:
    return Paragraph(text, STYLES["H1"])


def h2(text: str) -> Paragraph:
    return Paragraph(text, STYLES["H2"])


def bullet(text: str) -> Paragraph:
    return Paragraph(f"- {text}", STYLES["Bullet"])


def equation(text: str) -> Table:
    block = Preformatted(text.strip(), STYLES["Equation"])
    table = Table([[block]], colWidths=[6.55 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.55, colors.HexColor("#AFC7D8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def code_block(text: str) -> Table:
    block = Preformatted(text.strip(), STYLES["Code"])
    table = Table([[block]], colWidths=[6.55 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.45, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def callout(title: str, body: str, tone: str = "blue") -> Table:
    palette = {
        "blue": (LIGHT_BLUE, BLUE),
        "teal": (LIGHT_TEAL, TEAL),
        "gold": (LIGHT_GOLD, GOLD),
        "red": (LIGHT_RED, RED),
        "gray": (LIGHT_GRAY, MUTED),
    }
    background, accent = palette[tone]
    content = [
        p(title, "CalloutStrong"),
        Spacer(1, 3),
        p(body, "Callout"),
    ]
    table = Table([[content]], colWidths=[6.55 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.55, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def data_table(headers, rows, widths=None, small=False) -> Table:
    head = [p(str(cell), "TableHead") for cell in headers]
    style = "TableBodySmall" if small else "TableBody"
    body = [[p(str(cell), style) for cell in row] for row in rows]
    table = Table(
        [head] + body,
        colWidths=widths,
        repeatRows=1,
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def page_end(story: list) -> None:
    story.append(PageBreak())


def build_story() -> list:
    story: list = []

    # Cover
    story.append(Spacer(1, 0.18 * inch))
    story.append(
        p(
            "REFEREE MANUSCRIPT &nbsp;&nbsp; / &nbsp;&nbsp; "
            + RELEASE_DATE.upper(),
            "CoverMeta",
        )
    )
    story.append(Spacer(1, 0.33 * inch))
    story.append(
        p(
            "A Candidate for an Unconditional<br/>"
            "Computer-Assisted Proof of",
            "Title",
        )
    )
    story.append(
        p(
            "the de Bruijn-Newman Upper Bound",
            "Subtitle",
        )
    )
    result_box = Table(
        [[p("Lambda &lt;= 0.1787854", "CoverResult")]],
        colWidths=[6.55 * inch],
        rowHeights=[0.92 * inch],
        hAlign="LEFT",
    )
    result_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 1.0, NAVY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story.append(result_box)
    story.append(Spacer(1, 0.34 * inch))
    story.append(
        callout(
            "Status boundary",
            "This is a computer-assisted unconditional proof that has not "
            "yet been peer reviewed. It is not a peer-reviewed theorem and "
            "is not a proof of the Riemann hypothesis. The peer-review "
            "boundary is load-bearing.",
            "red",
        )
    )
    story.append(Spacer(1, 0.28 * inch))
    cover_meta = [
        ["Prepared for", "Adversarial mathematical and computational review"],
        ["Prepared by", "Jude Gomila"],
        [
            "Primary repository",
            f'<link href="{REPOSITORY_URL}">{REPOSITORY_URL}</link>',
        ],
        [
            "Evidence binding",
            "PDF listed in repository SHA256SUMS; use the exact accompanying "
            "Git commit",
        ],
    ]
    story.append(
        data_table(
            ["Field", "Value"],
            cover_meta,
            widths=[1.35 * inch, 5.2 * inch],
            small=True,
        )
    )
    story.append(Spacer(1, 0.15 * inch))
    story.append(
        p(
            "The manuscript summarizes the proof architecture and review "
            "contract. The repository source files and published references "
            "remain authoritative.",
            "Caption",
        )
    )
    page_end(story)

    # Abstract and status
    story.append(h1("Abstract and review status"))
    story.append(
        p(
            "This manuscript presents a referee package for a proposed "
            "computer-assisted upper bound on the de Bruijn-Newman constant. "
            "The proposed argument instantiates Theorem 1.2 of D. H. J. "
            "Polymath with exact parameters, uses the published "
            "Platt-Trudgian finite verification of the Riemann hypothesis, "
            "and supplies new finite-window, all-N tail, and closed-barrier "
            "arguments with directed interval certificates.",
            "Lead",
        )
    )
    story.append(
        equation(
            """
X       = 6000000185827
t0      = 129/800 = 0.16125
y0^2    = 87677/2500000 = 0.0350708

t0 + y0^2/2 = 893927/5000000 = 0.1787854
"""
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        p(
            "If every cited theorem is applicable, every new analytic lemma "
            "is correct, and every implementation faithfully certifies its "
            "stated predicate, the assembled argument would establish "
            "Lambda &lt;= 0.1787854 without assuming an unproved conjecture. "
            "Those antecedents have not yet been independently confirmed."
        )
    )
    story.append(
        data_table(
            ["The package claims", "The package does not claim"],
            [
                [
                    "An exact candidate theorem and a complete internal "
                    "dependency chain.",
                    "Independent acceptance of any new analytic reduction.",
                ],
                [
                    "Directed interval certificates for every encoded "
                    "finite, tail, and barrier gate.",
                    "A proof of the Riemann hypothesis or Lambda = 0.",
                ],
                [
                    "Fresh replay paths and a fail-closed release seal.",
                    "Peer review, publication, novelty, or public priority.",
                ],
                [
                    "A proposed unconditional logical form.",
                    "That green software output alone proves unconditionality.",
                ],
            ],
            widths=[3.275 * inch, 3.275 * inch],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        callout(
            "Decision requested from the referee",
            "Audit the published-theorem applications, handwritten analytic "
            "reductions, proof-to-code maps, and directed computations as "
            "separate layers. Report whether each of the three exact "
            "Polymath criterion hypotheses is established.",
            "gold",
        )
    )
    page_end(story)

    # TOC
    story.append(h1("Contents"))
    toc = TableOfContents()
    toc.levelStyles = [STYLES["TOC0"], STYLES["TOC1"]]
    story.append(toc)
    story.append(Spacer(1, 10))
    story.append(
        callout(
            "How to use this manuscript",
            "Sections 1-9 state the proposed mathematics. Sections 10-12 "
            "describe evidence, replay, and review procedure. Sections 13-14 "
            "state the residual risks and disposition. The "
            "appendices bind headline values to repository paths.",
            "blue",
        )
    )
    page_end(story)

    # 1
    story.append(h1("1. Criterion and exact candidate row"))
    story.append(
        p(
            "Let H_t denote the heat-flow deformation of the Riemann xi "
            "function in the normalization used by the Polymath paper. The "
            "de Bruijn-Newman constant Lambda is characterized by the "
            "property that the zeros of H_t are all real precisely for "
            "t &gt;= Lambda. The proposed proof uses the upper-bound criterion "
            "in Polymath Theorem 1.2 rather than attempting a new global "
            "characterization."
        )
    )
    story.append(
        data_table(
            ["Item", "Exact value", "Role"],
            [
                ["Barrier abscissa X", "6000000185827", "Criterion site"],
                ["Required zeta height", "X/2", "Hypothesis (i)"],
                ["Time t0", "129/800", "Final time and barrier top"],
                ["Height square y0^2", "87677/2500000", "Criterion geometry"],
                [
                    "Candidate bound",
                    "893927/5000000",
                    "t0 + y0^2/2",
                ],
                ["Final y ceiling", "sqrt(271/400)", "Hypothesis (ii)"],
            ],
            widths=[1.7 * inch, 2.1 * inch, 2.75 * inch],
        )
    )
    story.append(h2("Three hypotheses to be supplied"))
    story.append(
        data_table(
            ["Criterion leg", "Exact domain", "Proposed supplier"],
            [
                [
                    "(i) verified height",
                    "0 &lt;= T &lt;= X/2; sigma to the right of 1/2",
                    "Platt-Trudgian plus exact H0/xi sign map",
                ],
                [
                    "(ii) final-time region",
                    "x &gt;= X+sqrt(1-y0^2), y0 &lt;= y &lt;= sqrt(1-2t0)",
                    "Finite Triangle windows plus all-N tail",
                ],
                [
                    "(iii) curved barrier",
                    "0 &lt;= t &lt;= t0 on the criterion barrier",
                    "Closed rectangular zero-free certificate",
                ],
            ],
            widths=[1.35 * inch, 2.7 * inch, 2.5 * inch],
            small=True,
        )
    )
    story.append(Spacer(1, 7))
    story.append(
        equation(
            """
y0^2 + 2 t0 = 893927/2500000 < 1
y0^2 < 1 - 2 t0 = 271/400
0 < t0 < 1/2,  X >= 200
"""
        )
    )
    story.append(
        p(
            "All parameter identities and domain containments are checked "
            "with exact rational arithmetic before the final assembly can "
            "reach its conclusion."
        )
    )
    page_end(story)

    # 2
    story.append(h1("2. Proof architecture and dependency discipline"))
    story.append(
        p(
            "The proposed argument is deliberately split into cited inputs, "
            "new mathematics, numerical realizations, stored evidence, and a "
            "final logical weld. No numerical transcript is permitted to "
            "stand in for an unstated theorem."
        )
    )
    story.append(
        data_table(
            ["Layer", "Object", "Failure meaning"],
            [
                [
                    "Published input",
                    "Polymath Theorems 1.2 and 1.3; Platt-Trudgian Theorem 1",
                    "Candidate cannot be assembled as stated",
                ],
                [
                    "New analytic layer",
                    "Native binding, Dini transfer, window freeze, tail, "
                    "derivative and barrier lemmas",
                    "Mathematical gap even if every replay is green",
                ],
                [
                    "Implementation",
                    "C/FLINT/Arb and Python interval programs",
                    "Proof-to-code correspondence failure",
                ],
                [
                    "Evidence",
                    "Finite shards, tail logs, coefficient and prism records",
                    "Stored certificate is incomplete or inconsistent",
                ],
                [
                    "Assembly",
                    "verify_assembly_1787854.py",
                    "One or more exact criterion legs is not supplied",
                ],
            ],
            widths=[1.25 * inch, 3.25 * inch, 2.05 * inch],
            small=True,
        )
    )
    story.append(h2("Dependency flow"))
    story.append(
        equation(
            """
Platt-Trudgian verified height ---------------------------> (i)

finite rows -> native binding -> all-y transfer
            -> window freeze -> effective error --+
                                                   +-----> (ii)
all-N tail theorem -> 256/512-bit Arb certificate --+

stored coefficients -> uniform error -> derivatives
                    -> 883 closed prisms -> winding ------> (iii)

(i) + (ii) + (iii) + exact rational substitution
    -> candidate conclusion Lambda <= 0.1787854
"""
        )
    )
    story.append(Spacer(1, 7))
    story.append(
        callout(
            "Fail-closed rule",
            "Malformed evidence, missing rows, nonconsecutive seams, interval "
            "overlap at a strict comparison, unexpected output, environment "
            "overrides, and manifest drift are fatal. A failed gate cannot be "
            "downgraded to a warning by the final assembly.",
            "teal",
        )
    )
    page_end(story)

    # 3
    story.append(h1("3. Verified-height hypothesis"))
    story.append(
        p(
            "Platt and Trudgian rigorously verify, using interval arithmetic, "
            "that every nontrivial zeta zero through height "
            "T_PT = 3000175332800 lies on the critical line. The candidate "
            "criterion needs information only through X/2."
        )
    )
    story.append(
        equation(
            """
T_PT = 3000175332800
X/2  = 6000000185827/2 = 3000000092913.5

T_PT - X/2 = 350479773/2 = 175239886.5 > 0
"""
        )
    )
    story.append(h2("Normalization and sign map"))
    story.append(
        p(
            "A zero H_0(x+iy)=0 first maps to a zero of xi at "
            "(1-y+ix)/2. The xi functional equation followed by conjugation "
            "produces the representative (1+y+ix)/2 required by the "
            "criterion. The affine identities are checked over exact "
            "rationals by verifiers/verify_criterion_sign_map.py."
        )
    )
    story.append(
        p(
            "The cited finite verification handles positive ordinate. At "
            "T=0 and 0&lt;sigma&lt;1, the alternating eta series is strictly "
            "positive after grouping consecutive terms, while "
            "eta(sigma)=(1-2^(1-sigma)) zeta(sigma) has a strictly negative "
            "prefactor. Thus zeta(sigma)&lt;0; at sigma=1, zeta has a pole. "
            "This closes the real-height endpoint of hypothesis (i)."
        )
    )
    story.append(
        data_table(
            ["Check", "Result"],
            [
                ["x-to-height normalization", "x = 2T"],
                ["critical line", "y = 0"],
                ["required real part", "(1+y0)/2 &gt; 1/2"],
                ["upper endpoint", "s = 1 is a pole, not a zeta zero"],
                ["height surplus", "350479773/2"],
            ],
            widths=[2.35 * inch, 4.2 * inch],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        callout(
            "Cited theorem boundary",
            "The repository does not re-prove the Platt-Trudgian computation. "
            "The referee must verify that its published theorem has exactly "
            "the strength and normalization consumed here.",
            "gold",
        )
    )
    page_end(story)

    # 4
    story.append(h1("4. Finite final-time corpus"))
    story.append(
        p(
            "At t=t0 the finite lane assigns one half-open x-window to each "
            "integer N from 690988 through 3840000. Fifteen compressed "
            "certificate shards contain exactly one successful row for every "
            "N, with no gap, duplicate, overlap, nonpositive row, or UNCERT "
            "record."
        )
    )
    story.append(
        data_table(
            ["Family", "Auxiliary primes", "N range", "Rows", "Stored minimum"],
            [
                [
                    "P11",
                    "2,3,5,7,11",
                    "690988..728999",
                    "38,012",
                    "0.000000791366",
                ],
                [
                    "P7",
                    "2,3,5,7",
                    "729000..818999",
                    "90,000",
                    "0.000315112459",
                ],
                [
                    "P5",
                    "2,3,5",
                    "819000..1027999",
                    "209,000",
                    "0.000305788807",
                ],
                [
                    "P23",
                    "2,3",
                    "1028000..3840000",
                    "2,812,001",
                    "0.000309285478",
                ],
            ],
            widths=[
                0.55 * inch,
                1.2 * inch,
                1.45 * inch,
                0.85 * inch,
                1.45 * inch,
            ],
            small=True,
        )
    )
    story.append(Spacer(1, 7))
    story.append(
        equation(
            """
number of rows = 3840000 - 690988 + 1 = 3149013
global stored T floor = 0.000000791366 at N = 690988
effective error Emax <= 0.000000233494905212337849

finite margin >= 0.000000557871094787 > 0
"""
        )
    )
    story.append(h2("Independent finite checks"))
    story.append(
        p(
            "A fresh producer run regenerated and compared every canonical "
            "row. Thirty direct 256-bit singleton evaluations cover the "
            "weakest row, both sides of each prime-family transition, both "
            "sides of every compressed-shard joint, and the closed finite-tail "
            "overlap at N=3840000. The weakest direct row reproduces the "
            "stored floor."
        )
    )
    story.append(
        callout(
            "Tight margin",
            "The finite margin is rigorous but small. A reviewer should "
            "prioritize directed rounding, the native normalization units, "
            "the all-height transfer, and every source branch at the weakest "
            "P11 row.",
            "red",
        )
    )
    page_end(story)

    # 5
    story.append(h1("5. Native binding, height transfer, and window freeze"))
    story.append(
        p(
            "The stored Triangle floor must be connected to the normalized "
            "function f_t in Polymath Theorem 1.3 before its sign can be used. "
            "NATIVE_BINDING.md supplies exact real-coefficient Dirichlet "
            "convolutions for both Riemann-Siegel sums."
        )
    )
    story.append(
        equation(
            """
E A        = sum B_(N,n) n^(-s_*)
conj(E) C0 = sum A_(N,n) n^(-conj(s_*))

|f_t| >=
  [1 - g_N - sum_(n>=2)(|B_(N,n)|+g_N|A_(N,n)|)n^(-sigma_N)]
  / M_N - g_N C_N
"""
        )
    )
    story.append(
        p(
            "Positivity supplies the sign required when replacing |E| by its "
            "upper bound M_N and also rules out E=0. No second Euler-factor "
            "conversion is applied. The resulting T_N is in the same "
            "normalized units as the additive Theorem 1.3 error."
        )
    )
    story.append(h2("Conservative effective-error weld"))
    story.append(
        p(
            "The target proof does not use the 10.44 constant in displayed "
            "equation (24). Starting from Proposition 6.6(vi), it applies "
            "1+u &lt;= exp(u), enlarges x-8.52 to x-12 in the denominator, "
            "and combines the exact constants 3.58+6.92=10.50. "
            "ERROR_CONSTANT_WELD.md records the derivation and a fail-closed "
            "checker verifies all six numerical consumers."
        )
    )
    story.append(h2("Authoritative Arb error budget"))
    story.append(
        p(
            "The uniform effective-error budget Emax and the finite margin "
            "are certified authoritatively by the standalone FLINT/Arb "
            "program verifiers/verify_prop410_arb.c, run at 256 and 512 bits "
            "in the pinned container (transcripts logs/prop410_arb_256.log "
            "and logs/prop410_arb_512.log, strictly parsed as assembly "
            "prerequisite P17, with a twenty-mutation fail-closed suite). "
            "Every decisive inequality subtracts the exact rational bound "
            "and requires the whole resulting ball on the strict side. The "
            "mpmath.iv computation of the same budget, and its copy under "
            "independent/prop410/, are same-backend corroboration only."
        )
    )
    story.append(h2("All-y transfer"))
    story.append(
        p(
            "The direct upper-Dini proof retains the signed "
            "composite-divisor cancellation, exhausts 243, 81, 27, and 9 "
            "active sign cells for the four prime families, and gives worst "
            "ratio &lt;= 0.99999860767275095. Separate interval arguments prove "
            "the normalizer and kappa correction nonincreasing."
        )
    )
    story.append(h2("Corrected x-window minorant"))
    story.append(
        equation(
            """
Sigma(x,y) =
  (1+y)/2 + (t0/4) log(x/(4 pi))
  - t0/(2 x^2) [1-3y+4y(1+y)/x^2]_+

G(x,y) <= G_N(y)
K(x,y) <= K_N(y)
Sigma(x,y) >= Sigma_N(y)
"""
        )
    )
    story.append(
        p(
            "The plus sign before the logarithmic term is essential. The "
            "window-freeze theorem proves Sigma increasing in x, including "
            "across the positive-part kink. Exact pi and square-root bounds "
            "place X+sqrt(1-y0^2) strictly inside the N=690988 window."
        )
    )
    page_end(story)

    # 6
    story.append(h1("6. Infinite all-N tail theorem"))
    story.append(
        p(
            "The finite lane ends only after the complete N=3840000 window; "
            "the tail begins at the same closed cutoff. TAIL_LEMMA.md gives a "
            "quantified theorem for every N at or above this cutoff, the "
            "complete required height interval, and a closed time box "
            "containing t0. It is not a sampled extrapolation."
        )
    )
    story.append(
        data_table(
            ["Quantity", "Certified directed result"],
            [
                ["Closed cutoff", "N_* = 3840000"],
                ["Convolution head", "M = 153814"],
                ["Error head", "M_err = 3000"],
                ["Contraction", "D &lt; 0.999721"],
                ["Mollifier cap", "M_max &lt; 1.608290"],
                ["Normalized flow", "&gt; 0.0001735326089372"],
                ["Effective error", "&lt; 0.000000011671604"],
                ["Post-error margin", "&gt; 0.0001735209373337"],
            ],
            widths=[2.45 * inch, 4.1 * inch],
        )
    )
    story.append(h2("Reduction to the cutoff"))
    story.append(
        p(
            "An exact finite Dirichlet convolution is partitioned into "
            "disjoint routed classes. Endpoint-cap lemmas and checked "
            "derivative signs reduce all N to the cutoff. Moving floors and "
            "N/(d+1) terms are handled explicitly. The y transfer covers "
            "y0 through sqrt(1-2t0), and the complete t box is interval "
            "evaluated without assuming monotonicity in t."
        )
    )
    story.append(
        equation(
            """
|M_lambda(s_*) f_t - 1| <= D < 1

(1-D)/M_max - (e_A + e_B + e_C0)
    > 0.0001735209373337 > 0
"""
        )
    )
    story.append(
        p(
            "One standalone FLINT/Arb implementation run at 256 and 512 bits "
            "is the primary certificate and is independently parsed. Python "
            "interval runs at 160 and 256 bits provide a separate "
            "implementation and lineage check."
        )
    )
    page_end(story)

    # 7
    story.append(h1("7. Closed barrier: approximation and coefficient data"))
    story.append(
        p(
            "The proposed barrier certificate proves zero-freeness on a closed "
            "rectangle that contains the complete curved barrier required by "
            "Polymath Theorem 1.2."
        )
    )
    story.append(
        equation(
            """
R = [X, X+1] + i [1809/10000, 1]
0 <= t <= 129/800

H_t(z) != 0  for z in R
"""
        )
    )
    story.append(
        data_table(
            ["Barrier fact", "Certified value"],
            [
                [
                    "Floor-square margin",
                    "y0^2 - 0.1809^2 = 234599/100000000 &gt; 0",
                ],
                ["Riemann-Siegel index", "N = 690988 throughout the box"],
                [
                    "Total error using Proposition 6.6(vi) corollary",
                    "&lt; 0.000356523011600040",
                ],
                ["Common approximation allowance", "1/800 = 0.00125"],
                ["Stored complex matrix", "62 x 62"],
                ["Real components checked", "7688/7688 contained"],
                [
                    "Omitted Taylor tail",
                    "&lt; 1.954234593244762 x 10^-22",
                ],
            ],
            widths=[2.45 * inch, 4.1 * inch],
        )
    )
    story.append(h2("The t=0 endpoint"))
    story.append(
        p(
            "Polymath Theorem 1.3 is stated for positive t. The barrier note "
            "extends the inequality to t=0 on this fixed compact rectangle: "
            "dominated convergence gives continuity of H_t, the fixed "
            "Riemann-Siegel index makes f_t a finite continuous sum, the "
            "conservative majorant is continuous, and B_t and its reciprocal are "
            "continuous and nonzero."
        )
    )
    story.append(
        callout(
            "Coefficient provenance",
            "Each stored 20-decimal component is restored as a ball with "
            "radius 10^-20 max(1,|component|). A separate Arb producer "
            "regenerates every component inside that allowance; the "
            "factorial Taylor remainder is propagated into every barrier "
            "value.",
            "teal",
        )
    )
    page_end(story)

    # 8
    story.append(h1("8. Derivative bounds, closed prisms, and winding"))
    story.append(
        p(
            "At each exact time seam the producer encloses f_t on a cyclic "
            "boundary mesh. Uniform spatial and time derivative majorants "
            "control the complete rectangle and the complete proposed time "
            "prism. The acceptance gate is one strict interval inequality."
        )
    )
    story.append(
        p(
            "Although Polymath Lemma 8.4 is stated for t&gt;0, the fixed-N "
            "finite sums and their displayed derivatives are C1 on the "
            "closed box, with denominators and logarithm branches certified "
            "safe. Applying the lemma for t&gt;=epsilon and then taking "
            "epsilon down to zero therefore supplies the same derivative "
            "majorants at the initial seam."
        )
    )
    story.append(
        equation(
            """
M_i >
  D_(z,i) / [2 (num-1)]
  + D_(t,i) (t_(i+1)-t_i)
  + 0.00125
"""
        )
    )
    story.append(
        p(
            "The factor 1/2 follows from the nearer-endpoint convex-disk "
            "homotopy on each half-subedge. D_t is recomputed on the whole "
            "proposed prism, rather than sampled at its left endpoint. Every "
            "endpoint ball must exclude zero, every argument increment must "
            "lie strictly inside (-pi,pi), and the winding enclosure must lie "
            "strictly inside (-1/4,1/4)."
        )
    )
    story.append(
        data_table(
            ["Recorded barrier result", "Value"],
            [
                ["Closed time prisms", "883 consecutive"],
                ["Initial time", "exactly 0"],
                ["Final endpoint", "contains 129/800"],
                ["Minimum recomputed prism margin", "&gt; 0.519849894613872543"],
                [
                    "Aggregate winding enclosure",
                    "inside [-8.95,8.95] x 10^-13",
                ],
                ["Linux replay", "GCC / FLINT 3.0.1; 54 parser checks"],
                ["macOS replay", "Clang / FLINT 3.6.0; 54 parser checks"],
            ],
            widths=[2.55 * inch, 4.0 * inch],
        )
    )
    story.append(
        p(
            "The zero-avoiding spatial, time, and approximation homotopies "
            "carry winding zero from the stored polygon to H_t/B_t on the "
            "true boundary. Because B_t is nonzero, the argument principle "
            "gives no H_t zeros inside the rectangle throughout each prism."
        )
    )
    story.append(
        p(
            "The last stored dyadic prism may extend slightly beyond the "
            "exact t0. The theorem restricts that already-certified prism to "
            "its intersection with 0&lt;=t&lt;=129/800. Restriction only "
            "decreases the displacement allowance, and the uniform "
            "approximation estimate is used only through exact t0."
        )
    )
    page_end(story)

    # 9
    story.append(h1("9. Final theorem weld"))
    story.append(
        p(
            "The final assembly executes every stored prerequisite before "
            "checking the exact domains and reaching the canonical Polymath "
            "criterion weld."
        )
    )
    story.append(
        data_table(
            ["Hypothesis", "Proposed evidence", "Exact coverage result"],
            [
                [
                    "(i)",
                    "Published verified height plus sign map",
                    "X/2 is below T_PT by 350479773/2",
                ],
                [
                    "(ii), finite",
                    "3,149,013 rows plus binding and transfer",
                    "[x_*, x_3840001)",
                ],
                [
                    "(ii), tail",
                    "All-N tail theorem and Arb certificate",
                    "[x_3840000, infinity)",
                ],
                [
                    "(iii)",
                    "883-prism closed rectangle",
                    "Contains the entire curved barrier for 0 &lt;= t &lt;= t0",
                ],
            ],
            widths=[0.75 * inch, 2.75 * inch, 3.05 * inch],
            small=True,
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        equation(
            """
(i) + (ii) + (iii)
    => Lambda <= t0 + y0^2/2

       = 129/800 + (87677/2500000)/2
       = 893927/5000000
       = 0.1787854
"""
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        callout(
            "Conclusion",
            "The repository contains an internally complete proof "
            "chain. Peer review of the published-theorem applications, new "
            "lemmas, proof-to-code correspondence, and interval computations "
            "is the remaining step to theorem status.",
            "red",
        )
    )
    story.append(h2("No conjectural premise"))
    story.append(
        p(
            "The finite Platt-Trudgian result is a published computational "
            "theorem, not an assumption of the full Riemann hypothesis. Thus "
            "the logical form is unconditional. Calling the "
            "proof unconditional does not prejudge whether the new "
            "argument is correct."
        )
    )
    page_end(story)

    # 10
    story.append(h1("10. Evidence hierarchy and integrity seal"))
    story.append(
        p(
            "A computer-assisted proof must distinguish the proposition, its "
            "reduction, the implementation, the numerical evidence, the "
            "parser, and the release binding. Agreement in later layers "
            "cannot repair an error in an earlier one."
        )
    )
    story.append(
        data_table(
            ["Evidence level", "Question answered", "Principal artifact"],
            [
                ["1. Statement", "What mathematical fact is needed?", "Proof notes"],
                ["2. Reduction", "Why does a finite check suffice?", "New lemmas"],
                ["3. Implementation", "Does code encode that reduction?", "C/Python source"],
                ["4. Directed output", "Did strict inequalities hold?", "Logs/certificates"],
                ["5. Parser/assembly", "Was all evidence consumed?", "Fail-closed verifiers"],
                ["6. Release binding", "Which exact bytes were reviewed?", "SHA256SUMS + Git"],
            ],
            widths=[1.4 * inch, 2.65 * inch, 2.5 * inch],
            small=True,
        )
    )
    story.append(h2("Seal behavior"))
    story.append(
        p(
            "scripts/seal.py inventories every stable regular file except the "
            "manifest itself and explicitly transient roots. An unlisted file, "
            "missing file, digest mismatch, symlink, special file, malformed "
            "manifest entry, or forbidden build product is fatal. The "
            "manifest must be regenerated only after the final PDF and every "
            "source or documentation edit are complete."
        )
    )
    story.append(h2("Adversarial checks already represented"))
    for item in [
        "finite row gaps, duplicates, overlaps, nonpositive floors, and UNCERT records;",
        "direct singleton checks across every family and shard seam;",
        "tail precision agreement, malformed balls, wrong domains, and missing gates;",
        "barrier seam continuity, terminal coverage, winding, and coefficient provenance;",
        "ambient Python and barrier override variables that could weaken checking;",
        "sanitizer, compiler-warning, and negative-input paths for critical producers.",
    ]:
        story.append(bullet(item))
    story.append(
        callout(
            "Interpretation",
            "A green seal proves artifact identity. A green replay proves the "
            "encoded predicates. Neither result, by itself, validates the "
            "mathematical reductions.",
            "gold",
        )
    )
    page_end(story)

    # 11
    story.append(h1("11. Reproduction protocol"))
    story.append(h2("Level A: stored fail-closed verification"))
    story.append(
        code_block(
            """
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes -r requirements.txt
./verify.sh
"""
        )
    )
    story.append(
        p(
            "This checks the release seal, historical provenance subset, all "
            "stored finite rows, native binding, window freeze, tail, both "
            "barrier transcripts, sign map, and exact final assembly."
        )
    )
    story.append(h2("Level B: portable clean container"))
    story.append(
        code_block(
            """
docker build --platform linux/amd64 -t dbn-lambda-01787854-review .
mkdir -p replay/container-review
docker run --rm --platform linux/amd64 --network none --read-only \\
  --cap-drop ALL --security-opt no-new-privileges \\
  --user "$(id -u):$(id -g)" \\
  --tmpfs /tmp:rw,exec,nosuid,size=4g \\
  -e REVIEW_OUTPUT=/review-output/evidence \\
  -v "$PWD:/work:ro" \\
  -v "$PWD/replay/container-review:/review-output" \\
  -w /work dbn-lambda-01787854-review
"""
        )
    )
    story.append(h2("Levels C-E: fresh producers"))
    story.append(
        code_block(
            """
./scripts/run_barrier_replay.sh replay/barrier
./scripts/run_tail_arb.sh replay/tail_arb

review_image_id=$(docker image inspect --format '{{.Id}}' \\
  dbn-lambda-01787854-review)
IMAGE=dbn-lambda-01787854-review \\
EXPECTED_IMAGE_ID="$review_image_id" \\
  ./scripts/run_full_sweep.sh replay/full_sweep
"""
        )
    )
    story.append(
        p(
            "The full sweep regenerates all 3,149,013 finite rows. The barrier "
            "replay regenerates all 7,688 coefficient components, Taylor and "
            "uniform-error bounds, and all 883 prisms. The tail replay builds "
            "and runs the standalone Arb implementation at 256 and 512 bits."
        )
    )
    story.append(
        callout(
            "Resource orientation",
            "The sealed GitHub workflow required roughly one hour for each of "
            "its full-review and all-row lanes. Runtime is hardware-dependent; "
            "review conclusions must be attached to the exact commit and "
            "transcripts, not to timing values.",
            "blue",
        )
    )
    page_end(story)

    # 12
    story.append(h1("12. Referee protocol"))
    story.append(
        p(
            "The highest-value review is conceptual. Replaying code first can "
            "confirm package usability, but the proof decision should follow "
            "the dependency order below."
        )
    )
    story.append(
        data_table(
            ["Priority", "Referee task", "Decision to record"],
            [
                [
                    "1",
                    "Compare the exact parameter row and all three domains "
                    "with Polymath Theorem 1.2.",
                    "Correct theorem transcription and weld?",
                ],
                [
                    "2",
                    "Audit the closed-barrier derivative, interpolation, "
                    "winding, B_t, and t=0 arguments.",
                    "Complete zero-free homotopy?",
                ],
                [
                    "3",
                    "Check coefficient rounding, Taylor remainder, and "
                    "Theorem 1.3 error formulas.",
                    "Valid common 0.00125 allowance?",
                ],
                [
                    "4",
                    "Check native Triangle convolution, signs, normalization, "
                    "and source map.",
                    "Stored floor bounds normalized |f_t|?",
                ],
                [
                    "5",
                    "Check Dini transfer, window freeze, endpoint convention, "
                    "and finite-tail overlap.",
                    "Complete finite domain?",
                ],
                [
                    "6",
                    "Check all-N tail partition, caps, monotonicity, and "
                    "effective error.",
                    "Complete infinite domain?",
                ],
                [
                    "7",
                    "Reproduce decisive computations in a different build "
                    "environment.",
                    "Independent numerical agreement?",
                ],
            ],
            widths=[0.55 * inch, 4.15 * inch, 1.85 * inch],
            small=True,
        )
    )
    story.append(h2("Required final report"))
    for item in [
        "state separately whether hypotheses (i), (ii), and (iii) are established;",
        "identify any conjectural premise, circular check, or shared conceptual dependency;",
        "classify each finding as documentary, local, bound-invalidating, or fatal to the method;",
        "record exact file, line, commit, toolchain, and transcript references;",
        "state whether the package may advance beyond not-yet-peer-reviewed status.",
    ]:
        story.append(bullet(item))
    page_end(story)

    # 13
    story.append(h1("13. Risk register and trust boundary"))
    story.append(
        data_table(
            ["Risk", "Current mitigation", "Residual external question"],
            [
                [
                    "Published theorem mismatch",
                    "Versioned PDFs, theorem maps, exact sign-map checker",
                    "Does the cited statement exactly imply the consumed form?",
                ],
                [
                    "Finite normalization/sign error",
                    "Symbolic binding, source probes, direct rows",
                    "Is every inequality direction and unit correct?",
                ],
                [
                    "All-height or all-N gap",
                    "Dini cells, cap derivatives, exact endpoint coverage",
                    "Are all monotonicity and floor arguments valid?",
                ],
                [
                    "Barrier interpolation gap",
                    "Closed-prism derivative bounds and convex-disk proof",
                    "Does the homotopy cover every boundary/time point?",
                ],
                [
                    "Coefficient truncation",
                    "All 7,688 components regenerated inside restored balls",
                    "Does the generator implement the intended formula?",
                ],
                [
                    "Common implementation error",
                    "Multiple precisions, two platforms, Python/Arb paths",
                    "Are implementations independent enough?",
                ],
                [
                    "Artifact drift",
                    "Fail-closed SHA-256 stable-tree seal",
                    "Was the exact reviewed commit preserved?",
                ],
            ],
            widths=[1.35 * inch, 2.65 * inch, 2.55 * inch],
            small=True,
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        callout(
            "Most fragile numerical interfaces",
            "The finite margin is approximately 5.58 x 10^-7, the worst Dini "
            "ratio is close to one, and the tail contraction is close to one. "
            "Each is still strictly certified, but all deserve independent "
            "directed recomputation.",
            "red",
        )
    )
    story.append(h2("What remains outside the machine seal"))
    story.append(
        p(
            "The release seal cannot establish that the handwritten lemmas are "
            "true, that the code realizes them faithfully, that independent "
            "paths avoid a shared conceptual mistake, or that the work is "
            "novel and publishable. Those are precisely the external review "
            "boundary."
        )
    )
    page_end(story)

    # 14
    story.append(h1("14. Conclusion"))
    story.append(
        p(
            "The repository presents a coherent candidate theorem with exact "
            "parameters, three proposed criterion suppliers, fail-closed "
            "directed certificates, full finite regeneration, separate "
            "FLINT/Arb and Python tail implementations, dual-platform barrier "
            "transcripts, and a stable release seal."
        )
    )
    story.append(
        equation(
            """
PROPOSED RESULT

Lambda <= 893927/5000000 = 0.1787854
"""
        )
    )
    story.append(
        p(
            "The result is a computer-assisted proof that has not yet been "
            "peer reviewed. Its mathematical and computational "
            "interfaces are open for independent adversarial review."
        )
    )
    story.append(
        callout(
            "Release disposition",
            "Suitable for open adversarial review as an unconditional "
            "computer-assisted proof, not yet peer reviewed. Not suitable "
            "for a claim of theorem acceptance until independent "
            "mathematical and computational reports are complete.",
            "teal",
        )
    )
    story.append(h2("Recommended next actions"))
    for item in [
        "review this repository at one exact review commit;",
        "freeze that review commit and retain all GitHub replay artifacts;",
        "obtain a line-by-line theorem report and a separate clean-environment computation report;",
        "repair every finding and rerun the complete seal and producer suite;",
        "only then prepare a public immutable archive, preprint, and journal submission.",
    ]:
        story.append(bullet(item))
    page_end(story)

    # References
    story.append(h1("References"))
    refs = [
        (
            "[1] D. H. J. Polymath, <i>Effective approximation of heat flow "
            "evolution of the Riemann xi function, and a new upper bound for "
            "the de Bruijn-Newman constant</i>, Research in the Mathematical "
            "Sciences 6, 31 (2019), "
            '<link href="https://arxiv.org/abs/1904.12438v2">'
            "arXiv:1904.12438v2</link>. "
            "Reviewed file SHA-256 recorded in references/README.md."
        ),
        (
            "[2] D. Platt and T. Trudgian, <i>The Riemann hypothesis is true "
            "up to 3 x 10^12</i>, Bulletin of the London Mathematical Society "
            "53 (2021), 792-797, "
            '<link href="https://doi.org/10.1112/blms.12460">'
            "DOI 10.1112/blms.12460</link>, "
            '<link href="https://arxiv.org/abs/2004.09765v1">'
            "arXiv:2004.09765v1</link>. "
            "Reviewed file SHA-256 recorded in references/README.md."
        ),
        (
            "[3] Mosaic Intelligence, <i>A certified unconditional upper "
            "bound Lambda &lt;= 0.1875 for the de Bruijn-Newman constant</i>, "
            '<link href="https://doi.org/10.5281/zenodo.21175533">'
            "DOI 10.5281/zenodo.21175533</link>. Repository copy: "
            "references/dbn21a-main.pdf."
        ),
        (
            "[4] F. Johansson, <i>Arb: efficient arbitrary-precision "
            "midpoint-radius interval arithmetic</i>, IEEE Transactions on "
            "Computers 66 (2017), 1281-1292, "
            '<link href="https://doi.org/10.1109/TC.2017.2690633">'
            "DOI 10.1109/TC.2017.2690633</link>."
        ),
        (
            "[5] The FLINT team, <i>FLINT: Fast Library for Number Theory</i>. "
            '<link href="https://flintlib.org/">flintlib.org</link>. The '
            "primary replay uses FLINT 3.0.1; the macOS cross-toolchain "
            "transcript uses FLINT 3.6.0. See ENVIRONMENT.txt and Dockerfile."
        ),
    ]
    for ref in refs:
        story.append(Paragraph(ref, STYLES["Reference"]))
    story.append(Spacer(1, 8))
    story.append(
        callout(
            "Authoritative-source rule",
            "Transcribed theorem maps and repository notes are review aids. "
            "The versioned published papers remain authoritative for cited "
            "results.",
            "gold",
        )
    )
    page_end(story)

    # Appendix A
    story.append(h1("Appendix A. Exact numerical ledger"))
    story.append(
        data_table(
            ["Obligation", "Headline directed result", "Primary evidence"],
            [
                [
                    "Verified height",
                    "surplus 350479773/2",
                    "PROOF_NOTE.md; criterion assembly",
                ],
                [
                    "Finite corpus",
                    "3,149,013 rows; min 0.000000791366",
                    "15 gzip shards; verify_finite_and_binding.py",
                ],
                [
                    "Finite error",
                    "Emax &lt;= 0.000000233494905212337849",
                    "logs/prop410_arb_256.log and _512.log (Arb, "
                    "authoritative); logs/finite_and_binding.log",
                ],
                [
                    "Finite margin",
                    "&gt;= 0.000000557871094787",
                    "native binding and effective-error weld",
                ],
                [
                    "Dini transfer",
                    "ratio &lt;= 0.99999860767275095",
                    "180/256-bit direct Arb checks",
                ],
                [
                    "Tail contraction",
                    "D &lt; 0.999721",
                    "256/512-bit FLINT/Arb",
                ],
                [
                    "Tail margin",
                    "&gt; 0.0001735209373337",
                    "logs/tail_arb_256.log; tail_arb_512.log",
                ],
                [
                    "Barrier approximation",
                    "error &lt; 0.000356523011600040",
                    "barrier/certificates/uniform_error_256.log",
                ],
                [
                    "Coefficient matrix",
                    "7688/7688 components contained",
                    "storedsum_provenance.log",
                ],
                [
                    "Taylor remainder",
                    "&lt; 1.954234593244762 x 10^-22",
                    "storedsum_taylor_tail.log",
                ],
                [
                    "Closed barrier",
                    "883 prisms; margin &gt; 0.519849894613872543",
                    "two barrier_target_closed transcripts",
                ],
                [
                    "Final assembly",
                    "40 fail-closed assembly gates",
                    "logs/assembly_1787854.log",
                ],
            ],
            widths=[1.45 * inch, 2.35 * inch, 2.75 * inch],
            small=True,
        )
    )
    story.append(Spacer(1, 7))
    story.append(
        p(
            "Rounded values in this appendix are orientation summaries. The "
            "directed endpoints in the stored logs and source predicates "
            "control every strict comparison."
        )
    )
    page_end(story)

    # Appendix B
    story.append(h1("Appendix B. Repository map"))
    story.append(
        data_table(
            ["Path", "Review purpose"],
            [
                ["PROOF_NOTE.md", "End-to-end theorem chain and conclusion"],
                ["CANDIDATE_PARAMETERS.md", "Exact row, boxes, and margins"],
                ["OPEN_REVIEW_QUESTIONS.md", "Load-bearing referee decisions"],
                ["NATIVE_BINDING.md", "Triangle-to-normalized-function theorem"],
                [
                    "ERROR_CONSTANT_WELD.md",
                    "Conservative 10.50 Proposition 6.6(vi) reduction",
                ],
                ["WINDOW_FREEZE_THEOREM.md", "Uniform x directions and endpoints"],
                ["TAIL_LEMMA.md", "All-N, all-y infinite-lane theorem"],
                ["DERIVATIVE_BOX_LEMMA.md", "Uniform barrier derivatives"],
                ["BARRIER_CERTIFICATE.md", "Closed-prism and winding theorem"],
                ["certificates/", "Complete compressed finite corpus"],
                ["barrier/", "Coefficient, error, source, and prism evidence"],
                ["verifiers/", "Fail-closed parsers and independent checkers"],
                ["scripts/", "Container and producer replay entry points"],
                ["references/", "Versioned authoritative paper copies"],
                [
                    "ADVERSARIAL_REVIEW_PROTOCOL.md",
                    "Dependency blueprint and falsification protocol",
                ],
                ["SECURITY.md", "Security reporting and execution policy"],
                [
                    "CONTAINER_IMAGE.md",
                    "Pinned environment and exact verified image binding",
                ],
                ["SHA256SUMS", "Stable-tree release binding"],
            ],
            widths=[2.35 * inch, 4.2 * inch],
            small=True,
        )
    )
    story.append(h2("Paper regeneration"))
    story.append(
        code_block(
            """
python3 -m pip install --require-hashes -r paper/requirements.txt
python3 paper/generate_paper.py
mkdir -p tmp/pdfs/rendered
pdftoppm -png -r 150 \\
  output/pdf/dbn_lambda_01787854_candidate_audit.pdf \\
  tmp/pdfs/rendered/page
pdfinfo output/pdf/dbn_lambda_01787854_candidate_audit.pdf
"""
        )
    )
    story.append(
        p(
            "The generator uses ReportLab invariant mode and PDF standard "
            "fonts. The committed PDF must be rendered page by page and "
            "visually inspected before the final SHA-256 seal is written. "
            "Invariant metadata timestamps are synthetic; the visible date "
            "and accompanying Git commit identify the review snapshot."
        )
    )
    story.append(
        callout(
            "End of referee manuscript",
            "Please attach findings to the exact Git commit and distinguish "
            "artifact integrity, numerical replay, mathematical validity, and "
            "publication status.",
            "blue",
        )
    )

    return story


def generate() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = CandidateDocTemplate(
        str(OUTPUT),
        pagesize=LETTER,
        leftMargin=0.72 * inch,
        rightMargin=0.72 * inch,
        topMargin=0.68 * inch,
        bottomMargin=0.64 * inch,
        title=(
            "A Candidate for an Unconditional Computer-Assisted Proof "
            "of Lambda <= 0.1787854"
        ),
        author="Jude Gomila",
        subject="Referee manuscript and reproducibility record",
        creator="ReportLab; source paper/generate_paper.py",
        keywords=(
            "de Bruijn-Newman constant, computer-assisted proof, "
            "interval arithmetic, external review"
        ),
    )
    document.multiBuild(build_story(), canvasmaker=ReleaseCanvas)
    print(OUTPUT)


if __name__ == "__main__":
    generate()
