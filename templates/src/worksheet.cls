\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{worksheet}[2024/01/13 Handwriting Worksheet]

\LoadClass[landscape,60pt,extrafontsizes]{memoir}

\RequirePackage[T1]{fontenc}
\RequirePackage{calligra}
\RequirePackage{geometry}
\RequirePackage{nopageno}
\RequirePackage{lineno}
\RequirePackage{tikz}

\geometry{margin=1in, top=0.5in, bottom=0.5in}
\setlength\parindent{0pt}

\DoubleSpacing

\newcommand{\lowercaseheight}{0.65ex}
\newcommand{\uppercaseheight}{2.2ex}
\newcommand{\descenderdepth}{-0.8ex}
\newenvironment{drillsheet}{
    \centering
    % let the "line numbers" start directly at the text
    \setlength\linenumbersep{0pt}
    % let the "line numbers" be the grid
    \renewcommand{\thelinenumber}{
        \begin{tikzpicture}[overlay]
            % baseline
            \draw ((0,0) -- ++(\textwidth + \marginparsep,0);
            % lowercase height
            \draw [ultra thin] ((0,\lowercaseheight) -- ++(\textwidth + \marginparsep,0);
            % uppercase height
            \draw (0,\uppercaseheight) -- ++(\textwidth + \marginparsep,0);
            % descender depth
            \draw [ultra thin] (0,\descenderdepth) -- ++(\textwidth + \marginparsep,0);
        \end{tikzpicture}
    }
    \renewcommand\linenumberfont{\normalfont\color{black}}
    \begin{linenumbers}
        \color{black!25}
}{
    \end{linenumbers}
}
