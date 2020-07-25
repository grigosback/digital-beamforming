%%
%% This is file `ibtesis.cls' 
%%
%% The style has the following options
%% papel o screen.     papel se usa para imprimir - screen agrega links
%% preprint.           Cambia los m\'{a}rgenes para incluir m\'{a}s texto en cada p\'{a}gina
%% singlespacing-doublespacing Modifica el espacio entre l\'{\i}neas
%%
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ibtesis}[2010/10/25 v0.8 (a4 paper) IB - UnCuyo]%

\LoadClassWithOptions{book}

\RequirePackage{ifpdf}
\RequirePackage[english,spanish]{babel}
\RequirePackage{makeidx}
\RequirePackage{caption}
\RequirePackage{fnpos}

% Paquetes para simbolos y fonts usados en ecuaciones
\RequirePackage{amsmath}
\RequirePackage{bm}

\RequirePackage{graphicx}
\RequirePackage{color}
\RequirePackage{fancyhdr}
\RequirePackage{changepage}

% La opci\'{o}n `preprint' produce un texto con m\'{a}rgenes m\'{a}s chicos (m\'{a}s texto por p\'{a}gina)
\newif\ifDraft \Draftfalse
\DeclareOption{preprint}{\Drafttrue}

% La opcion predeterminada es interlineado de un espacio y medio
% El interlineado se puede cambiar con cualquiera de estas opciones
\DeclareOption{onehalfspace}{\gdef\@spacing{onehalfspacing}\gdef\@space{onehalfspace}}
\DeclareOption{singlespace} {\gdef\@spacing{singlespacing}\gdef\@space{singlespace}}
\DeclareOption{doublespace} {\gdef\@spacing{doublespacing}\gdef\@space{doublespace}}


% Las opciones paper/screen dan versiones muy similares. La versi\'{o}n screen incorpora informaci\'{o}n adicional en el documento y enlaces que no son necesarios o vistos en la versi\'{o}n impresa.
\newif\ifpapel \papelfalse
\DeclareOption{papel}{\papeltrue} 
\DeclareOption{screen}{\papelfalse} % En principio no se usa

\ExecuteOptions{papel,onehalfspace}
\ProcessOptions
\RequirePackage{calc}
\RequirePackage[a4paper]{geometry}
\RequirePackage[\@spacing]{setspace}


\newif\iftitlepage \titlepagetrue % initially true by default
% For preprint we do not create a title page (?)
\ifDraft\titlepagefalse\fi

% The Page layout depends on the mode final/preprint
\ifpapel%
\ifDraft\geometry{total={178mm,262mm},top=25mm, includefoot}%
\else\geometry{total={155mm,256mm},top=30mm, left=30mm, includefoot}\fi%
\else%
\ifDraft\geometry{total={178mm,262mm},top=25mm,ratio=1:1, includefoot}%
\else\geometry{total={155mm,256mm},top=30mm, hmarginratio=1:1, includefoot}\fi%
\fi

\RequirePackage{hyperref}
\ifpdf\ifpapel\hypersetup{pdfborder={0 0 0},
  pdfpagemode={UseOutlines},%
  pdfhighlight  =/N,%
  pdfstartview={FitH},  %% determines starting view ("percentage")
  colorlinks=false,
}\else%
\hypersetup{pdfborder={0 0 0},
  pdfpagemode={UseOutlines},%
  pdfhighlight  =/P,%
  pdfstartview={FitH},  %% determines starting view ("percentage")
  colorlinks=true,
  linkcolor=blue,
  anchorcolor=red,
  citecolor=green
}%
\fi
\fi

% Modificamos "\today" en espa\~{n}ol para que \date solo muestre el mes y el a\~{n}o.
\def\es@today#1{%
 \ifcase\es@datefmt
  \es@month#1%
 \else
  \es@month#1~\the\day
 \fi
 \ de\ifnum\year>1999\es@yearl\fi~\the\year}

% Modificado para que nos d\'{e} las p\'{a}ginas en romanos min\'{u}sculas (no s\'{e} que estoy haciendo ac\'{a})
\DeclareRobustCommand\es@scroman{\@firstofone}

% Usado internamente para chequear si se definieron algunos comandos
\def\@ifdefined#1#2{\@ifundefined{#1}{}{#2}}

% Algunas definiciones
\newcommand\directorname {Director}
\newcommand\codirectorname {Co-director}
\newcommand\juradoname {Miembros del Jurado}
\newcommand\jurado[2][1]{\gdef\@njurado{#1} \gdef\@jurado{#2}}
\def\grado#1{\gdef\@grado{#1}}
\def\carrera#1{\gdef\@carrera{#1}}
\def\director#1{\gdef\@director{#1}}
\def\codirector#1{\gdef\@codirector{#1}}
\def\laboratorio#1{\gdef\@laboratorio{#1}}
\def\palabrasclave#1{\gdef\@keywordsEspanol{#1}}
\def\keywords#1{\gdef\@keywordsIngles{#1}}

\newcommand\SetPdfInfo{\ifpdf\hypersetup{pdfauthor={\@author},
  pdftitle={\@carrera},
  pdfsubject={\@title},
  pdfkeywords={\@keywordsEspanol},
}\fi}

% Set default values
\author{Nombre del autor}
\director{Agregar Nombre del director}
\carrera{Tesis Carrera de Doctorado en F\'{\i}sica}
\grado{Doctorando o Maestrando}
\laboratorio{Lugar de trabajo - Centro At\'{o}mico Bariloche}
\palabrasclave{palabras, clave, espa\~{n}ol}
\keywords{key, words, English}

% Definimos la car\'{a}tula
\if@titlepage%
\renewcommand\maketitle{\pagenumbering{roman}%
\begin{titlepage}%
\ifpapel\begin{adjustwidth}{}{10.mm}\else\begin{adjustwidth}{2.5mm}{2.5mm}\fi
\large%
    \let\footnotesize\small
    \let\footnoterule\relax
    \let \footnote \thanks
    \begin{center}%   Carrera
      {\Large  \MakeUppercase \@carrera\\}
      \vskip 10ex%     Titulo
      {\bfseries \MakeUppercase \@title \par}%
      \vskip 10ex%     Autor
      % \vfill
      {%
        \begin{tabular}[t]{c}%
          \bfseries \@author \\ \bfseries \@grado
        \end{tabular}\par}%
      \vskip 8ex%    Director(es)
      {%
        \begin{center}
        \begin{tabular}[t]{cc}%
          \textbf{\@director}\\\directorname%    Director
        \end{tabular}%
      \hfill%
        \ifx\@codirector\undefined{}\else{%
          \begin{tabular}[t]{cc}%
            \textbf{\@codirector}\\\codirectorname%    Co-Director
          \end{tabular}%
          \par}%
        \fi%
      \end{center}
    }
    \ifx\@jurado\undefined{}\else{%     Jurado
      \vskip 4ex \vfill\begin{center}{\normalsize
          {\bfseries \juradoname}\\ 
       % \ifnum\@njurado=1 \begin{tabular}[t]{l}\else\begin{tabular}[t]{ll}\fi%
          \@jurado%
       % \end{tabular}%
      }\end{center}\par}\fi%
    \vskip 6ex%     Fecha
      {\@date \par}%       % Set date
{      \vskip 4ex \vfill%
      \@laboratorio
      \vskip 3em%
        Instituto Balseiro\\
        Universidad Nacional de Cuyo\\
        Comisi\'{o}n Nacional de Energ\'{\i}a At\'{o}mica\\
        Argentina
}    \end{center}\par
     \@thanks%
     \SetPdfInfo
\end{adjustwidth}\end{titlepage}%
\setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\director\@empty
  \global\let\codirector\@empty
  \global\let\grado\@empty
  \global\let\carrera\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
  \global\let\director\relax
  \global\let\codirector\relax
  \global\let\grado\relax
  \global\let\carrera\relax
}%
\fi


\pagestyle{fancy}%
\renewcommand{\chaptermark}[1]{\markboth{{#1}}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}

\fancypagestyle{plain}{% First page of chapter
\fancyhf{}%
\fancyfoot[C]{\bfseries\thepage}
\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}
}

\fancypagestyle{myheadings}{% Custom pages
\fancyhf{}%
\fancyhead{}%
\fancyfoot[C]{\bfseries\thepage}
\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}
}
% All other pages
\fancyhead[LO]{}
\fancyfoot[L,R,C]{}
\fancyhead[LE,RO]{\bfseries\thepage}
\fancyhead[RE]{\sffamily\bfseries\nouppercase{\leftmark}}
\fancyhead[LO]{\sffamily\nouppercase{\rightmark}}
\renewcommand{\headrulewidth}{1pt}

% Redefino el comando \cleardoublepage  para que no ponga ni header ni footer 
% en las paginas vacias que quedan entre capitulos. Copiado de fancyhdr.tex
% Solo funciona para el draft
\def\cleardoublepage{\clearpage\ifDraft\else\if@twoside \ifodd\c@page\else
  \hbox{}
  \vspace*{\fill}
  \vspace{\fill}
  \thispagestyle{empty}
  \newpage
  \if@twocolumn\hbox{}\newpage\fi\fi\fi\fi}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%   From gatech-thesis.cls   %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%    New formatting environments and commands.
% \newcommand{\setfrontpagestyle}[1]{%
%   \gdef\front@pagestyle{#1}
% }
% \newcommand{\setbodypagestyle}[1]{%
%   \gdef\body@pagestyle{#1}
% }
% \newcommand{\setbackpagestyle}[1]{%
%   \gdef\back@pagestyle{#1}
% }

%
%% \begin{preliminary} sets the pagestyle and pagenumbering 
%% (roman numeral format ) for the preliminary sections; 
%% \end{preliminary} resets the pagenumbering. To start page 
%% numbering in arabic format, use \pagestyle{plain} and 
%% \pagenumbering{arabic} after the preliminary environment block
%% The spacing within preliminary is not affected by options
\newenvironment{preliminary}%
{  
  \frontmatter
  \begin{singlespace}
  \pagenumbering{roman}%
  \pagestyle{plain}%
  \iftitlepage\maketitle\fi%
  \end{singlespace}
  \begin{\@space}
}%
{%
  \end{\@space}
  \ifDraft%
  \else%
  \if@twoside%
  \if@openright%
  \cleardoublepage%
  \fi%
  \fi%
  \fi%
  \newpage%
  \pagenumbering{arabic}%
  \pagestyle{fancy}%
  \mainmatter %
}%

%% \begin{postliminary} sets the pagestyle for the
%% postliminary sections.  
%%
%% \end{postliminary} resets the pagestyle and
%% performs any other cleanup.
\newenvironment{postliminary}%
  {  \cleardoublepage%
    \pagestyle{empty}}%
  {%
% \settocdepth{\chapter@tocdepth}%
   \pagestyle{fancy}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%% Arreglamos las listas del principio %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand\tableofcontents{%
   \if@twocolumn
      \@restonecoltrue\onecolumn
   \else
      \@restonecolfalse
   \fi
   \cleardoublepage
   \phantomsection
   \addcontentsline{toc}{chapter}{\contentsname}%
   \chapter*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
   \@starttoc{toc}%
   \if@restonecol\twocolumn\fi}

\renewcommand\listoffigures{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \cleardoublepage
    \phantomsection
    \addcontentsline{toc}{chapter}{\listfigurename}%
    \chapter*{\listfigurename}%
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}%
    \@starttoc{lof}%
    \if@restonecol\twocolumn\fi
    }

\renewcommand\listoftables{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \cleardoublepage
    \phantomsection
    \addcontentsline{toc}{chapter}{\listtablename}%
    \chapter*{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    \if@restonecol\twocolumn\fi
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Definimos el estilo de los captions
\captionsetup{width=0.95\textwidth,textfont=footnotesize,labelfont={bf,small}} 

\newcommand\dedicatoria[1]{%
\cleardoublepage
\thispagestyle{empty}
\vspace*{10em}%
\begin{flushright} \large
\begin{tabular}[t]{l}  #1 \end{tabular}
\end{flushright}
\cleardoublepage
}

\newcommand\agradecimientos[1]{%
\cleardoublepage
\section*{Agradecimientos}%
 #1
\vfill
\cleardoublepage
}

\newenvironment{resumen}{\cleardoublepage%
\phantomsection%
\markboth{\abstractname}{}
\addcontentsline {toc}{chapter}{\abstractname}%
\chapter*{\abstractname}%
\noindent}%
{\vfill%
{\noindent {\bfseries Palabras clave:} \MakeUppercase \@keywordsEspanol}% \vfill%
\cleardoublepage}

\newenvironment{abstract}{\cleardoublepage%
\phantomsection%
\markboth{\abstractnameeng}{}
\addcontentsline {toc}{chapter}{\abstractnameeng}%
\selectlanguage{english}%
\chapter*{\abstractnameeng}%
\noindent}%
{\vfill%
{\noindent {\bfseries Keywords:} \MakeUppercase \@keywordsIngles}% \vfill%
\selectlanguage{spanish}%
\cleardoublepage}

\newenvironment{abreviaturas}{\cleardoublepage%
\phantomsection%
\markboth{\nomname}{}%
\addcontentsline {toc}{chapter}{\nomname}%
\chapter*{\nomname}}%
{\cleardoublepage}

\newenvironment{seccion}[1]{\cleardoublepage%
\phantomsection%
\markboth{#1}{}%
\addcontentsline {toc}{chapter}{#1}%
\chapter*{#1}}%
{\cleardoublepage}

\newenvironment{biblio}{\cleardoublepage%
\phantomsection%
\addcontentsline {toc}{chapter}{\bibname}}%
{\cleardoublepage}

\date{\Today}

\DeclareRobustCommand{\chapterquote}[2]{%
  \begin{adjustwidth}{0.3\textwidth}{}%
    \noindent{\em ``#1''} \newline%
  \indent --- #2%
  \end{adjustwidth}%
  \vspace{.5cm}%
}

\setlength{\headheight}{15.6pt}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Declaraciones \'{u}tiles %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newlength{\imsizeL}\setlength{\imsizeL}{0.9\textwidth}
\newlength{\imsize}\setlength{\imsize}{0.7\textwidth}
\newlength{\imsizeS}\setlength{\imsizeS}{0.5\textwidth}

\addto\captionsspanish{
\def\nomname{\'{I}ndice de s{\'{\i}}mbolos}
\def\contentsname{\'{I}ndice de contenidos}
\def\listfigurename{\'{I}ndice de figuras}
\def\listtablename{\'{I}ndice de tablas}
\def\figurename{Figura}
\def\tablename{Tabla}
\def\abstractname{Resumen}
\def\abstractnameeng{Abstract}
\def\bibname{Bibliograf{\'{\i}}a}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\endinput

