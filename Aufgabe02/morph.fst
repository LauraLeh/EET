%%% FLEXIONSKLASSEN NOMEN %%%

%% KLASSE [-(e)s/-e]
% Genitiv Singular Endungen:
% -es, wenn Nomen auf -s, -ß, -x oder -z enden z.B. das Glas -> des Glases
% -s in allen anderen Fällen

$noun-es-e$ = <Noun>:<> (\
{<nom><sg>}:{} |\
{<gen><sg>}:{<insert-e>s} |\
{<dat><sg>}:{e} |\
{<acc><sg>}:{} |\
{<nom><pl>}:{e} |\
{<gen><pl>}:{e} |\
{<dat><pl>}:{en} |\
{<acc><pl>}:{e})

% KLASSE [-s/-s]

$noun-s-s$ = <Noun>:<> (\
{<nom><sg>}:{} |\
{<gen><sg>}:{s} |\
{<dat><sg>}:{} |\
{<acc><sg>}:{} |\
{<nom><pl>}:{s} |\
{<gen><pl>}:{s} |\
{<dat><pl>}:{s} |\
{<acc><pl>}:{s})

%%% FLEXIONSKLASSE VERBEN  %%%

% KLASSE [regelmäßig, indikativ]
% pres = Präsens, past = Präteritum

$verb-reg$ = <Verb>:<> (\
{<base>}:{en} |\
{<1sg><pres>}:{e} |\
{<2sg><pres>}:{st} |\
{<3sg><pres>}:{t} |\
{<1pl><pres>}:{en} |\
{<2pl><pres>}:{t} |\
{<3pl><pres>}:{en} |\
{<1sg><past>}:{te} |\
{<2sg><past>}:{test} |\
{<3sg><past>}:{te} |\
{<1pl><past>}:{ten} |\
{<2pl><past>}:{tet} |\
{<3pl><past>}:{ten})


%%% FLEXIONSKLASSEN ADJEKTIVE %%%
% Superlativ mit "am": z.B. (am) schnellsten.
% Nicht gemeint ist der Superlativ mit Artikel, z.B. die schnellste

% KLASSE [regelmäßig]

$adj-reg$ = <Adjective>:<> (\
{<basis>}:{} |\
{<compar>}:{er} |\
{<superl>}:{sten})

% KLASSE [Endung -el]
% Bei Komparativ entfällt ein e: dunkel -> dunkler (statt dunkeler)

$adj-el$ = <Adjective>:<> (\
{<basis>}:{} |\
{<compar>}:{<del-e>er} |\
{<superl>}:{sten})

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

$morph$ = "noun-es-e.lex" $noun-es-e$ |\
"noun-s-s.lex" $noun-s-s$ |\
"verb-reg.lex" $verb-reg$ |\
"adj-reg.lex" $adj-reg$ |\
"adj-el.lex" $adj-el$

ALPHABET = [A-Za-zäöüÄÖÜß] <del-e> <insert-e>:<>
$noun-insert-e$ = (<insert-e>:e) ^-> ([sßxz] __ s)

ALPHABET = [A-Za-zäöüÄÖÜß] <del-e>:<>
$adj-del-e$ = (e:<>) ^-> (__ l<del-e>)

$morph$ || $noun-insert-e$ || $adj-del-e$
