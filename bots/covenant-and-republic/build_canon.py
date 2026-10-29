#!/usr/bin/env python3
import concurrent.futures
import json
import re
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path

OUT_DIR = Path("/workspace/constitution-bot")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CANON = [
    # I. BIBLICAL, HEBRAIC & CHRISTIAN COVENANTAL FOUNDATIONS
    {
        "id": "bib-genesis-imago-dei",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Genesis 1:26–27 & 9:6 (KJV) — Imago Dei & Natural Equality",
        "author": "Moses (Pentateuch)",
        "date": "Ancient / 1611 KJV",
        "url": "https://www.biblegateway.com/passage/?search=Genesis+1%3A26-27%2C+Genesis+9%3A6&version=KJV",
        "significance": "Establishes that all men are created in the image of God, grounding ontological moral equality, the sanctity of human life, and the legitimacy of civil magistrates executing capital justice before any human state existed."
    },
    {
        "id": "bib-exodus-jethro-decalogue",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Exodus 18:13–26 & 20:1–17 (KJV) — Jethro's Counsel & The Moral Law (Decalogue)",
        "author": "Moses (Pentateuch)",
        "date": "Ancient / 1611 KJV",
        "url": "https://www.biblegateway.com/passage/?search=Exodus+18%3A13-26%2C+Exodus+20%3A1-17&version=KJV",
        "significance": "Models representative, tiered judicial federalism ('able men, such as fear God, men of truth, hating covetousness') and codifies the moral law protecting life, family, private property, and truthful testimony."
    },
    {
        "id": "bib-deuteronomy-constitutionalism",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Deuteronomy 1:13–17; 16:18–20; 17:14–20; 19:15 (KJV) — Hebraic Constitutionalism",
        "author": "Moses (Pentateuch)",
        "date": "Ancient / 1611 KJV",
        "url": "https://www.biblegateway.com/passage/?search=Deuteronomy+1%3A13-17%3B+16%3A18-20%3B+17%3A14-20%3B+19%3A15&version=KJV",
        "significance": "Identified by political scientist Donald S. Lutz as the single most frequently cited book in American political literature from 1760–1805: mandates consent in choosing wise magistrates, impartial justice, two-or-three-witness due process, and a ruler bound under written higher law."
    },
    {
        "id": "bib-1samuel-8-monarchy",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "1 Samuel 8:10–18 (KJV) — Warning Against Concentrated Royal Power & Standing Extraction",
        "author": "Samuel (Prophets)",
        "date": "Ancient / 1611 KJV",
        "url": "https://www.biblegateway.com/passage/?search=1+Samuel+8%3A10-18&version=KJV",
        "significance": "Central scriptural text of Thomas Paine's Common Sense, Jonathan Mayhew's sermons, and New England clergy condemning hereditary monarchy, standing armies, eminent domain abuse, and confiscatory taxation."
    },
    {
        "id": "bib-isaiah-33-22-jeremiah-17-9",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Isaiah 33:22 & Jeremiah 17:9 (KJV) — Threefold Functions of Rule & Human Depravity",
        "author": "Isaiah & Jeremiah",
        "date": "Ancient / 1611 KJV",
        "url": "https://www.biblegateway.com/passage/?search=Isaiah+33%3A22%3B+Jeremiah+17%3A9&version=KJV",
        "significance": "Isaiah 33:22 ('The Lord is our judge, the Lord is our lawgiver, the Lord is our king') was repeatedly cited alongside Montesquieu in Founding-era sermons on separated powers, while Jeremiah 17:9 grounded the Christian realist view of fallen human nature ('If men were angels, no government would be necessary,' Federalist No. 51)."
    },
    {
        "id": "bib-nt-civil-authority",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Matthew 22:15–22; Acts 5:29; Romans 13:1–7; 1 Peter 2:13–17; Galatians 5:1 (KJV)",
        "author": "New Testament Apostles",
        "date": "1st Century AD / 1611 KJV",
        "url": "https://www.biblegateway.com/passage/?search=Matthew+22%3A15-22%3B+Acts+5%3A29%3B+Romans+13%3A1-7%3B+1+Peter+2%3A13-17%3B+Galatians+5%3A1&version=KJV",
        "significance": "Separates the jurisdiction of Caesar from the jurisdiction of God, defines legitimate civil magistrates as 'ministers of God for good' to punish evildoers, and establishes the duty to obey God rather than men when civil power commands tyranny."
    },
    {
        "id": "chr-aquinas-treatise-on-law",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Summa Theologiae, Prima Secundae, Questions 90–97 (Treatise on Law)",
        "author": "Thomas Aquinas",
        "date": "c. 1265–1274",
        "url": "https://lonang.com/library/reference/aquinas-summa-theologica/",
        "significance": "Defines the fourfold hierarchy of Eternal, Natural, Human, and Divine Law, establishing that an unjust human enactment contrary to natural and divine law is 'no law at all, but rather a species of violence.'"
    },
    {
        "id": "chr-calvin-institutes-book-4-ch-20",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Institutes of the Christian Religion, Book IV, Chapter 20 (Of Civil Government)",
        "author": "John Calvin",
        "date": "1536 / 1559",
        "url": "https://lonang.com/library/reference/1536-jc/",
        "significance": "Formulated the doctrine of interposition by 'lesser magistrates' against tyrannical kings and praised mixed aristocratic-popular republicanism as the safest form of civil polity given human sinfulness."
    },
    {
        "id": "chr-vindiciae-contra-tyrannos",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Vindiciae, Contra Tyrannos (A Defense of Liberty Against Tyrants)",
        "author": "Stephanus Junius Brutus (Philippe du Plessis-Mornay / Hubert Languet)",
        "date": "1579",
        "url": "https://lonang.com/library/reference/vindiciae-contra-tyrannos-1579/",
        "significance": "Huguenot covenant treatise proving from Old Testament history and Roman law that kings hold office under a double covenant with God and the people, and forfeit obedience when they subvert the law."
    },
    {
        "id": "chr-rutherford-lex-rex",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Lex, Rex, or The Law and the Prince",
        "author": "Samuel Rutherford",
        "date": "1644",
        "url": "https://lonang.com/library/reference/rutherford-lex-rex/",
        "significance": "Scottish Covenanter masterpiece inverting Rex Lex ('the king is law') into Lex, Rex ('the law is king'), arguing from Scripture and natural law that sovereignty originates in God through the people and that lawless rulers may be resisted."
    },
    {
        "id": "chr-milton-areopagitica-tenure",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Areopagitica (1644) & The Tenure of Kings and Magistrates (1649)",
        "author": "John Milton",
        "date": "1644 / 1649",
        "url": "https://www.gutenberg.org/ebooks/608",
        "significance": "Defended freedom of the press against prior restraint so truth could contend openly with falsehood, and argued from natural law and Scripture that all men are born naturally free with the right to depose tyrants."
    },
    {
        "id": "chr-sandoz-political-sermons",
        "category": "I. Biblical, Hebraic & Christian Covenantal Foundations",
        "title": "Political Sermons of the American Founding Era, 1730–1805 (incl. Elisha Williams 1744, Jonathan Mayhew 1750, Samuel Davies 1755, John Witherspoon 1776, Samuel West 1776, Abraham Keteltas 1777)",
        "author": "Edited by Ellis Sandoz (Liberty Fund)",
        "date": "1730–1805",
        "url": "https://oll.libertyfund.org/titles/sandoz-political-sermons-of-the-american-founding-era-1730-1805-2-vols",
        "significance": "The definitive primary collection of 55 Founding-era pulpit sermons—including Mayhew's Discourse Concerning Unlimited Submission (which John Adams called the 'catechism' of the Revolution) and Witherspoon's Dominion of Providence—demonstrating how colonial clergy preached natural rights, resistance to tyranny, and constitutional self-government."
    },

    # II. CLASSICAL ANTIQUITY & NATURAL LAW REPUBLICS
    {
        "id": "cls-aristotle-politics",
        "category": "II. Classical Antiquity & Natural Law Republics",
        "title": "Politics & Nicomachean Ethics",
        "author": "Aristotle",
        "date": "c. 350 BC",
        "url": "https://classics.mit.edu/Aristotle/politics.html",
        "significance": "Distinguished true constitutional regimes (monarchy, aristocracy, polity) aimed at the common good from their corruptions (tyranny, oligarchy, mob democracy) and argued that the rule of dispassionate law must prevail over the rule of men."
    },
    {
        "id": "cls-polybius-histories-book6",
        "category": "II. Classical Antiquity & Natural Law Republics",
        "title": "The Histories, Book VI (On the Mixed Roman Constitution & Anacyclosis)",
        "author": "Polybius",
        "date": "c. 150 BC",
        "url": "https://www.perseus.tufts.edu/hopper/text?doc=Plb.+6.1",
        "significance": "Primary classical blueprint studied by John Adams (Defence of the Constitutions) and James Madison for institutional checks and balances combining monarchical (executive), aristocratic (senatorial), and democratic (popular) elements to arrest regime decay."
    },
    {
        "id": "cls-cicero-republic-laws-duties",
        "category": "II. Classical Antiquity & Natural Law Republics",
        "title": "De Re Publica (On the Commonwealth), De Legibus (On the Laws), & De Officiis (On Duties)",
        "author": "Marcus Tullius Cicero",
        "date": "54–44 BC",
        "url": "https://www.gutenberg.org/ebooks/54161",
        "significance": "Called by Thomas Jefferson part of the 'elementary books of public right' behind the Declaration; gave the definitive classical definition of natural law as 'right reason in agreement with nature,' universal, immutable, and superior to Senate or popular decrees."
    },
    {
        "id": "cls-plutarch-parallel-lives",
        "category": "II. Classical Antiquity & Natural Law Republics",
        "title": "Parallel Lives of the Noble Grecians and Romans",
        "author": "Plutarch",
        "date": "c. 100 AD",
        "url": "https://classics.mit.edu/Browse/browse-Plutarch.html",
        "significance": "The biographical handbook of the Founders—providing the classical pseudonyms ('Publius' from Publicola, 'Brutus', 'Cato', 'Helvidius', 'Pacificus') and exemplars of republican civic virtue (Lycurgus, Solon, Cato the Younger)."
    },

    # III. ENGLISH COMMON LAW & CONSTITUTIONAL MILESTONES
    {
        "id": "eng-magna-carta-1215",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "Magna Carta (The Great Charter of Liberties)",
        "author": "English Barons & King John",
        "date": "June 15, 1215",
        "url": "https://avalon.law.yale.edu/medieval/magframe.asp",
        "significance": "Fountainhead of Anglo-American rule of law: subjected the monarch to written law, barred taxation without common counsel, and established in Chapters 39–40 the guarantee of trial by peers and 'law of the land' (due process)."
    },
    {
        "id": "eng-coke-institutes-bonham",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "Institutes of the Lawes of England (1628–1644) & Dr. Bonham's Case (1610)",
        "author": "Sir Edward Coke",
        "date": "1610–1644",
        "url": "https://www.gutenberg.org/ebooks/58338",
        "significance": "Trained Jefferson, Adams, Otis, and Patrick Henry in the common law; declared that 'a man's house is his castle,' opposed general warrants, and asserted in Bonham's Case that acts against common right and reason are void—precursor to judicial review."
    },
    {
        "id": "eng-petition-of-right-1628",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "The Petition of Right",
        "author": "Parliament of England (drafted by Sir Edward Coke)",
        "date": "June 7, 1628",
        "url": "https://avalon.law.yale.edu/17th_century/england.asp",
        "significance": "Reaffirmed Magna Carta against Charles I by prohibiting non-parliamentary taxation, arbitrary imprisonment without cause shown (habeas corpus), quartering of soldiers in private homes (Third Amendment), and peacetime martial law."
    },
    {
        "id": "eng-habeas-corpus-1679",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "Habeas Corpus Act of 1679",
        "author": "Parliament of England",
        "date": "May 27, 1679",
        "url": "https://press-pubs.uchicago.edu/founders/documents/a1_9_2s2.html",
        "significance": "Codified the Great Writ against executive detention without speedy judicial review, enshrined directly in Article I, Section 9, Clause 2 of the U.S. Constitution."
    },
    {
        "id": "eng-bill-of-rights-1689",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "The English Bill of Rights (An Act Declaring the Rights and Liberties of the Subject)",
        "author": "Parliament of England",
        "date": "December 16, 1689",
        "url": "https://avalon.law.yale.edu/17th_century/england.asp",
        "significance": "Direct structural ancestor of the U.S. Bill of Rights: barred royal suspension of laws, peacetime standing armies without legislative consent, infringement of the right to keep arms for defense, and excessive bail or cruel and unusual punishments."
    },
    {
        "id": "eng-blackstone-commentaries",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "Commentaries on the Laws of England (4 Volumes)",
        "author": "Sir William Blackstone",
        "date": "1765–1769",
        "url": "https://lonang.com/library/reference/blackstone-commentaries-law-england/",
        "significance": "Second most cited secular author of the Founding era (after Montesquieu); synthesized English common law on natural law ('no human laws are of any validity, if contrary to this'), absolute rights of personal security, personal liberty, and private property, and criminal procedure."
    },
    {
        "id": "eng-delolme-constitution-england",
        "category": "III. English Common Law & Constitutional Milestones",
        "title": "The Constitution of England",
        "author": "Jean-Louis de Lolme",
        "date": "1771 / 1775",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch11s7.html",
        "significance": "Celebrated by John Adams as the sharpest analysis of balanced government, bicameralism, executive unity, judicial independence, and liberty of the press."
    },

    # IV. NATURAL RIGHTS, CLASSICAL WHIG & SCOTTISH COMMON SENSE PHILOSOPHY
    {
        "id": "phi-grotius-pufendorf-burlamaqui-vattel",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "The Law of Nature and Nations Canon: Grotius (1625), Pufendorf (1672), Burlamaqui (1747), & Emer de Vattel's The Law of Nations (1758)",
        "author": "Hugo Grotius, Samuel von Pufendorf, Jean-Jacques Burlamaqui, Emer de Vattel",
        "date": "1625–1758",
        "url": "https://lonang.com/library/reference/vattel-law-of-nations/",
        "significance": "Supplied the Founders' vocabulary on 'the Laws of Nature and of Nature's God,' the inalienable right to pursue happiness (Burlamaqui), sovereign equality of states, treaty power, letters of marque, and the law of war and neutrality (Vattel)."
    },
    {
        "id": "phi-locke-second-treatise-toleration",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "Two Treatises of Government (Second Treatise, quoting Richard Hooker) & A Letter Concerning Toleration",
        "author": "John Locke",
        "date": "1689",
        "url": "https://lonang.com/library/reference/locke-two-treatises-government/",
        "significance": "Provided the philosophical architecture of the Declaration of Independence and Fifth Amendment: state of nature governed by natural law, property grounded in self-ownership and labor, government as a fiduciary trust by consent, legislative supremacy subject to natural rights, the right of revolution, and freedom of religious conscience."
    },
    {
        "id": "phi-sidney-discourses-government",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "Discourses Concerning Government",
        "author": "Algernon Sidney",
        "date": "1698 (written 1680–1683)",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch3s1.html",
        "significance": "Whig martyr treatise paired by Jefferson with Locke as the core authority on popular sovereignty, condemning patriarchal divine right (Filmer) and defending armed citizens and popular resistance to tyranny."
    },
    {
        "id": "phi-cato-letters",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "Cato's Letters: Or, Essays on Liberty, Civil and Religious, and Other Important Subjects",
        "author": "John Trenchard & Thomas Gordon",
        "date": "1720–1723",
        "url": "https://oll.libertyfund.org/titles/trenchard-catos-letters-4-vols-in-2-lf-ed",
        "significance": "Reprinted across colonial newspapers more than almost any other secular work; taught extreme vigilance against executive corruption, standing armies, public debt schemes, and suppression of free speech ('Freedom of Speech is the great Bulwark of Liberty,' Letter No. 15)."
    },
    {
        "id": "phi-montesquieu-spirit-of-laws",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "The Spirit of the Laws (De l'Esprit des Lois, esp. Book XI, Ch. 6 & Book IX)",
        "author": "Charles-Louis de Secondat, Baron de La Brède et de Montesquieu",
        "date": "1748",
        "url": "https://lonang.com/library/reference/montesquieu-spirit-of-laws/",
        "significance": "The single most cited secular thinker of the Founding era (cited by both Federalists and Anti-Federalists): formulated the functional separation of legislative, executive, and judicial powers and the theory of the confederate republic."
    },
    {
        "id": "phi-scottish-enlightenment-hutcheson-hume-smith-reid",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "Scottish Moral & Political Philosophy: Francis Hutcheson, David Hume's Essays (1741–1752), Adam Smith's Moral Sentiments (1759) & Wealth of Nations (1776), and Thomas Reid",
        "author": "Francis Hutcheson, David Hume, Adam Smith, Thomas Reid",
        "date": "1725–1785",
        "url": "https://oll.libertyfund.org/titles/hume-essays-moral-political-literary-lf-ed",
        "significance": "Shaped the Founders' epistemology of 'self-evident truths' (Scottish Common Sense Realism taught by Witherspoon at Princeton), free-market commercial liberty against mercantilism (Smith), and Madison's extended-republic theory of faction in Federalist No. 10 (Hume's 'Idea of a Perfect Commonwealth')."
    },
    {
        "id": "phi-beccaria-crimes-punishments",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "On Crimes and Punishments",
        "author": "Cesare Beccaria",
        "date": "1764",
        "url": "https://www.gutenberg.org/ebooks/58700",
        "significance": "Copied extensively into Jefferson's and Adams's commonplace books; shaped the Fourth, Fifth, Sixth, and Eighth Amendments on proportional punishment, public speedy trials, and prohibition of torture and cruel punishments."
    },
    {
        "id": "phi-burke-conciliation-reflections",
        "category": "IV. Natural Rights, Classical Whig & Scottish Common Sense Philosophy",
        "title": "Speech on Conciliation with the Colonies (1775) & Reflections on the Revolution in France (1790)",
        "author": "Edmund Burke",
        "date": "1775 / 1790",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch1s2.html",
        "significance": "Explained why American colonists' fierce devotion to English common-law charters, Protestant Christianity, and legal education made parliamentary coercion futile, and contrasted American ordered constitutional liberty with the atheistic, leveling terror of the French Revolution."
    },

    # V. COLONIAL CHARTERS, COVENANTS & EARLY SELF-GOVERNMENT (1606–1754)
    {
        "id": "col-virginia-charter-1606",
        "category": "V. Colonial Charters, Covenants & Early Self-Government (1606–1754)",
        "title": "First Charter of Virginia",
        "author": "King James I",
        "date": "April 10, 1606",
        "url": "https://avalon.law.yale.edu/17th_century/va01.asp",
        "significance": "Guaranteed that American colonists and their posterity should enjoy 'all Liberties, Franchises, and Immunities... as if they had been abiding and borne, within this our Realme of England'—the legal bedrock of colonial constitutionalism."
    },
    {
        "id": "col-mayflower-compact-1620",
        "category": "V. Colonial Charters, Covenants & Early Self-Government (1606–1754)",
        "title": "The Mayflower Compact",
        "author": "Pilgrim Settlers at Plymouth",
        "date": "November 11, 1620",
        "url": "https://avalon.law.yale.edu/17th_century/mayflower.asp",
        "significance": "America's first written civil covenant—formed 'in the Presence of God and one of another' to 'covenant and combine ourselves together into a civil Body Politick' to enact 'just and equal Laws' for the general good."
    },
    {
        "id": "col-fundamental-orders-ct-1639",
        "category": "V. Colonial Charters, Covenants & Early Self-Government (1606–1754)",
        "title": "The Fundamental Orders of Connecticut",
        "author": "Thomas Hooker & Freemen of Windsor, Hartford, and Wethersfield",
        "date": "January 14, 1639",
        "url": "https://avalon.law.yale.edu/17th_century/order.asp",
        "significance": "Inspired by Rev. Thomas Hooker's sermon that 'the foundation of authority is laid, firstly, in the free consent of the people'; recognized as the first complete written constitution in history creating a representative government."
    },
    {
        "id": "col-mass-body-of-liberties-1641",
        "category": "V. Colonial Charters, Covenants & Early Self-Government (1606–1754)",
        "title": "The Massachusetts Body of Liberties",
        "author": "Nathaniel Ward & Massachusetts General Court",
        "date": "December 1641",
        "url": "https://history.hanover.edu/texts/masslib.html",
        "significance": "Contained 98 enumerated liberties anticipating the U.S. Bill of Rights by 150 years: due process, equal protection, just compensation for taken property, bail, jury trial, protection against double jeopardy, and ban on cruel bodily punishments."
    },
    {
        "id": "col-maryland-rhode-island-penn-charters",
        "category": "V. Colonial Charters, Covenants & Early Self-Government (1606–1754)",
        "title": "Maryland Toleration Act (1649), Rhode Island Royal Charter (1663), & William Penn's Frame of Government (1682) and Charter of Privileges (1701)",
        "author": "Colonial Assemblies, Roger Williams, & William Penn",
        "date": "1649–1701",
        "url": "https://avalon.law.yale.edu/17th_century/pa01.asp",
        "significance": "Pioneered liberty of religious conscience ('a flourishing civil state may stand and best be maintained with a full liberty in religious concernments'), written amendment clauses (invented by William Penn), and the right of criminal defendants to call witnesses."
    },
    {
        "id": "col-albany-plan-1754",
        "category": "V. Colonial Charters, Covenants & Early Self-Government (1606–1754)",
        "title": "The Albany Plan of Union",
        "author": "Benjamin Franklin & Albany Congress",
        "date": "July 10, 1754",
        "url": "https://avalon.law.yale.edu/18th_century/albany.asp",
        "significance": "First formal proposal for a federal union of the American colonies under a Grand Council apportioned by colonial contribution while preserving each colony's internal constitution."
    },

    # VI. REVOLUTIONARY PAMPHLETS, RESOLVES & CONTINENTAL CONGRESS (1761–1776)
    {
        "id": "rev-otis-writs-rights-1761-1764",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "Speech Against Writs of Assistance (1761) & The Rights of the British Colonies Asserted and Proved (1764)",
        "author": "James Otis Jr.",
        "date": "February 1761 / 1764",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch2s5.html",
        "significance": "John Adams wrote of Otis's 1761 courtroom argument against general search warrants: 'Then and there the child Independence was born'; directly inspired the Fourth Amendment and asserted that an Act of Parliament against natural equity is void."
    },
    {
        "id": "rev-stamp-act-resolves-1765",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "Virginia Stamp Act Resolves & Declaration of Rights and Grievances of the Stamp Act Congress",
        "author": "Patrick Henry & Stamp Act Congress",
        "date": "May–October 1765",
        "url": "https://avalon.law.yale.edu/18th_century/resolu65.asp",
        "significance": "Asserted that taxation by an unrepresentative Parliament destroys British and natural liberty and that trial in juryless vice-admiralty courts subverts the common law."
    },
    {
        "id": "rev-dickinson-farmer-letters-1767",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "Letters from a Farmer in Pennsylvania",
        "author": "John Dickinson",
        "date": "1767–1768",
        "url": "https://www.gutenberg.org/ebooks/48546",
        "significance": "United the colonies against the Townshend Acts by proving that any parliamentary revenue tax without consent makes colonists 'slaves' because 'those who are taxed without their own consent, expressed by themselves or their representatives, are slaves.'"
    },
    {
        "id": "rev-sam-adams-rights-of-colonists-1772",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "The Rights of the Colonists (Report of the Boston Committee of Correspondence)",
        "author": "Samuel Adams",
        "date": "November 20, 1772",
        "url": "https://history.hanover.edu/texts/adamss.html",
        "significance": "Synthesized natural rights ('First, a Right to Life; Secondly, to Liberty; Thirdly, to Property; together with the Right to support and defend them'), Christian liberty, and English constitutional rights four years before Jefferson's Declaration."
    },
    {
        "id": "rev-jefferson-summary-view-1774",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "A Summary View of the Rights of British America",
        "author": "Thomas Jefferson",
        "date": "July 1774",
        "url": "https://avalon.law.yale.edu/18th_century/jeffsumm.asp",
        "significance": "Argued that Parliament had zero legislative authority over the colonies, rehearsed the list of royal grievances later placed in the Declaration, and concluded: 'The God who gave us life gave us liberty at the same time; the hand of force may destroy, but cannot disjoin them.'"
    },
    {
        "id": "rev-continental-congress-1774-1775",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "Declaration and Resolves of the First Continental Congress (1774), Articles of Association (1774), & Declaration of the Causes and Necessity of Taking Up Arms (1775)",
        "author": "First & Second Continental Congress (John Jay, John Dickinson, Thomas Jefferson)",
        "date": "October 1774 – July 1775",
        "url": "https://avalon.law.yale.edu/18th_century/resolves.asp",
        "significance": "Grounded colonial rights simultaneously in 'the immutable laws of nature, the principles of the English constitution, and the several charters or compacts' and justified armed defensive resistance before God and the world."
    },
    {
        "id": "rev-paine-common-sense-1776",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "Common Sense",
        "author": "Thomas Paine",
        "date": "January 10, 1776",
        "url": "https://www.gutenberg.org/ebooks/147",
        "significance": "Shattered lingering allegiance to King George III using 1 Samuel 8 and natural-rights reasoning, proclaiming that 'in America THE LAW IS KING.'"
    },
    {
        "id": "rev-john-adams-thoughts-on-government-1776",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "Thoughts on Government",
        "author": "John Adams",
        "date": "April 1776",
        "url": "https://TeachingAmericanHistory.org/document/thoughts-on-government/",
        "significance": "Written to counter unicameral leveling schemes; became the structural blueprint for the new state constitutions and the 1787 U.S. Constitution (bicameral legislature, independent executive with veto, and life-tenured independent judiciary)."
    },
    {
        "id": "rev-virginia-declaration-of-rights-1776",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "The Virginia Declaration of Rights",
        "author": "George Mason (with James Madison on Article 16)",
        "date": "June 12, 1776",
        "url": "https://www.archives.gov/founding-docs/virginia-declaration-of-rights",
        "significance": "Direct textual model for both the Declaration of Independence and the federal Bill of Rights; Madison amended Article 16 from 'toleration' to the natural right of 'the free exercise of religion, according to the dictates of conscience'; Article 15 warned that 'no free government, or the blessings of liberty, can be preserved to any people, but by a firm adherence to justice, moderation, temperance, frugality, and virtue, and by frequent recurrence to fundamental principles.'"
    },
    {
        "id": "rev-declaration-of-independence-1776",
        "category": "VI. Revolutionary Pamphlets, Resolves & Continental Congress Documents (1761–1776)",
        "title": "The Unanimous Declaration of the Thirteen United States of America",
        "author": "Thomas Jefferson, John Adams, Benjamin Franklin, Roger Sherman, Robert R. Livingston, & Second Continental Congress",
        "date": "July 4, 1776",
        "url": "https://www.archives.gov/founding-docs/declaration-transcript",
        "significance": "The moral and philosophical charter of the United States ('the apple of gold' inside the Constitution's 'picture of silver,' as Lincoln described it): grounds American sovereignty in 'the Laws of Nature and of Nature's God,' Creator-endowed unalienable rights, consent of the governed, 27 constitutional grievances against executive/legislative tyranny, and reliance on Divine Providence."
    },

    # VII. THE CONFEDERATION PERIOD, STATE CONSTITUTIONS & FOUNDATIONAL STATUTES (1776–1787)
    {
        "id": "cnf-massachusetts-constitution-1780",
        "category": "VII. The Confederation Period & Foundational State Constitutions (1776–1787)",
        "title": "The Constitution of the Commonwealth of Massachusetts",
        "author": "John Adams (ratified by popular town vote)",
        "date": "1780",
        "url": "https://malegislature.gov/Laws/Constitution",
        "significance": "Oldest functioning written constitution in the world and primary state template for the 1787 federal Constitution; Article XXX established the classic mandate separating legislative, executive, and judicial powers 'to the end it may be a government of laws and not of men.'"
    },
    {
        "id": "cnf-articles-of-confederation-1777",
        "category": "VII. The Confederation Period & Foundational State Constitutions (1776–1787)",
        "title": "Articles of Confederation and Perpetual Union",
        "author": "Second Continental Congress (committee led by John Dickinson)",
        "date": "Adopted Nov 15, 1777 / Ratified Mar 1, 1781",
        "url": "https://www.archives.gov/milestone-documents/articles-of-confederation",
        "significance": "America's first national frame of government; established state sovereignty (Article II), Privileges and Immunities comity (Article IV), and Full Faith and Credit, while exposing the defects of a league lacking an executive, judiciary, commerce power, or direct taxation."
    },
    {
        "id": "cnf-madison-memorial-jefferson-statute-1785-1786",
        "category": "VII. The Confederation Period & Foundational State Constitutions (1776–1787)",
        "title": "Memorial and Remonstrance Against Religious Assessments (1785) & The Virginia Statute for Religious Freedom (1786)",
        "author": "James Madison (1785) & Thomas Jefferson (drafted 1777, enacted Jan 16, 1786)",
        "date": "1785–1786",
        "url": "https://lonang.com/library/reference/remonstrance-religious-assessments-1785/",
        "significance": "Essential primary evidence for the original meaning of the First Amendment Religion Clauses: Madison declared that duty to the Creator is 'precedent, both in order of time and in degree of obligation, to the claims of Civil Society,' and Jefferson affirmed that 'Almighty God hath created the mind free.'"
    },
    {
        "id": "cnf-adams-defence-of-constitutions-1787",
        "category": "VII. The Confederation Period & Foundational State Constitutions (1776–1787)",
        "title": "A Defence of the Constitutions of Government of the United States of America (3 Vols.)",
        "author": "John Adams",
        "date": "1787–1788",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch11s10.html",
        "significance": "Circulated on the floor of the 1787 Philadelphia Convention; refuted French unicameralism (Turgot) through exhaustive analysis of ancient and modern republics, proving that unchecked power in any single assembly inevitably produces tyranny."
    },
    {
        "id": "cnf-madison-vices-1787",
        "category": "VII. The Confederation Period & Foundational State Constitutions (1776–1787)",
        "title": "Vices of the Political System of the United States",
        "author": "James Madison",
        "date": "April 1787",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch5s16.html",
        "significance": "Madison's pre-Convention diagnostic memo identifying the 12 structural defects of the Confederation and state legislatures (multiplicity, mutability, and injustice of state laws violating minority and property rights), laying the groundwork for the Virginia Plan and Federalist No. 10."
    },
    {
        "id": "cnf-northwest-ordinance-1787",
        "category": "VII. The Confederation Period & Foundational State Constitutions (1776–1787)",
        "title": "The Northwest Ordinance (An Ordinance for the Government of the Territory of the United States North-West of the River Ohio)",
        "author": "Confederation Congress (Nathan Dane, Manasseh Cutler, Rufus King)",
        "date": "July 13, 1787 (re-enacted by the First Congress, Aug 7, 1789)",
        "url": "https://www.archives.gov/milestone-documents/northwest-ordinance",
        "significance": "One of the four organic laws of the United States: admitted new states on an equal footing with original states, enacted a national bill of rights (habeas corpus, jury trial, proportionate representation, contract clause), banned slavery in the Northwest Territory (Article VI), and declared in Article III: 'Religion, morality, and knowledge, being necessary to good government and the happiness of mankind, schools and the means of education shall forever be encouraged.'"
    },

    # VIII. JOURNALS, NOTES & DRAFTS OF THE CONSTITUTIONAL CONVENTION (MAY–SEPT 1787)
    {
        "id": "cnv-farrand-records-madison-notes-1787",
        "category": "VIII. Journals, Notes & Drafts of the Constitutional Convention (May–Sept 1787)",
        "title": "The Records of the Federal Convention of 1787 (4 Vols., ed. Max Farrand) — incl. Official Journal of William Jackson, James Madison's Notes of Debates, and Notes of Robert Yates, Rufus King, James McHenry, William Paterson, William Pierce, & Alexander Hamilton",
        "author": "James Madison, William Jackson, et al. (ed. Max Farrand)",
        "date": "May 25 – September 17, 1787",
        "url": "https://avalon.law.yale.edu/subject_menus/debcont.asp",
        "significance": "The complete day-by-day primary record of the framing of the Constitution—covering the Virginia Plan, New Jersey Plan, Connecticut (Sherman) Compromise, Committee of Detail draft (Rutledge/Wilson), Committee of Style draft (Gouverneur Morris), and every clause-by-clause vote."
    },
    {
        "id": "cnv-us-constitution-1787",
        "category": "VIII. Journals, Notes & Drafts of the Constitutional Convention (May–Sept 1787)",
        "title": "The Constitution of the United States of America",
        "author": "Philadelphia Constitutional Convention (ratified by 'We the People' in State Conventions)",
        "date": "Signed September 17, 1787 / Effective 1788–1789",
        "url": "https://www.archives.gov/founding-docs/constitution-transcript",
        "significance": "The supreme written law of the land (Article VI): establishes a federal republic of enumerated legislative powers (Article I), a unitary energetic Executive (Article II), an independent Article III Judiciary, horizontal separation of powers, vertical federalism, and protection of republican self-government."
    },

    # IX. THE RATIFICATION DEBATES: FEDERALISTS, ANTI-FEDERALISTS & STATE CONVENTIONS (1787–1790)
    {
        "id": "rat-federalist-papers-1787-1788",
        "category": "IX. The Ratification Debates: Federalists, Anti-Federalists & State Conventions (1787–1790)",
        "title": "The Federalist Papers (All 85 Essays by 'Publius')",
        "author": "Alexander Hamilton (51), James Madison (29), & John Jay (5)",
        "date": "October 27, 1787 – August 1788",
        "url": "https://avalon.law.yale.edu/subject_menus/fed.asp",
        "significance": "The premier contemporaneous exposition of the Constitution's original public meaning and political theory—especially Nos. 1 (choice versus accident and force), 9–10 (extended republic & faction), 39 (compound federal/national republic), 45 (powers delegated to federal government are 'few and defined'), 47–51 (separation of powers & 'ambition must be made to counteract ambition'), 68–70 (energetic unitary executive), 78 (judicial review & judiciary as 'least dangerous' branch with 'neither FORCE nor WILL, but merely judgment'), and 84 (danger of reading enumerated bills of rights as implying unenumerated powers)."
    },
    {
        "id": "rat-anti-federalist-papers-1787-1788",
        "category": "IX. The Ratification Debates: Federalists, Anti-Federalists & State Conventions (1787–1790)",
        "title": "The Anti-Federalist Papers (ed. Herbert J. Storing) — Brutus, Federal Farmer, Centinel, Cato, Agrippa, Pennsylvania Minority, Luther Martin (Genuine Information), George Mason (Objections), & Patrick Henry",
        "author": "Brutus (likely Robert Yates), Federal Farmer, George Mason, Patrick Henry, Luther Martin, Mercy Otis Warren, et al.",
        "date": "1787–1788",
        "url": "https://press-pubs.uchicago.edu/founders/documents/v1ch8s13.html",
        "significance": "Prophetic warnings against consolidation under the Necessary and Proper Clause, General Welfare Clause, Supremacy Clause, and an unaccountable federal judiciary (especially Brutus Nos. I & XI–XV)—directly forced the adoption of the Bill of Rights and the Tenth Amendment."
    },
    {
        "id": "rat-elliots-debates-1787-1788",
        "category": "IX. The Ratification Debates: Federalists, Anti-Federalists & State Conventions (1787–1790)",
        "title": "The Debates in the Several State Conventions on the Adoption of the Federal Constitution (5 Vols., 'Elliot's Debates')",
        "author": "Edited by Jonathan Elliot",
        "date": "1787–1788 (published 1836)",
        "url": "https://memory.loc.gov/ammem/amlaw/lwed.html",
        "significance": "James Madison insisted that the true constitutional meaning must be sought not in secret Philadelphia notes alone, but in the state ratifying conventions where 'We the People' breathed life into the document (especially Pennsylvania with James Wilson, Virginia with Madison, Marshall, Henry, and Mason, and New York with Hamilton and Melancton Smith)."
    },

    # X. THE BILL OF RIGHTS, EARLY PRACTICE, TREATISES & DICTIONARIES (1755–1868)
    {
        "id": "bor-bill-of-rights-maclay-annals-1789-1791",
        "category": "X. The Bill of Rights, Early Constitutional Practice, Treatises & Dictionaries",
        "title": "The Bill of Rights (Amendments I–X), Madison's June 8, 1789 Speech, Annals of the First Congress, & Journal of William Maclay (1789–1791)",
        "author": "James Madison & First U.S. Congress / Sen. William Maclay",
        "date": "Proposed Sept 25, 1789 / Ratified Dec 15, 1791",
        "url": "https://www.archives.gov/founding-docs/bill-of-rights-transcript",
        "significance": "Enshrined explicit declaratory barriers against federal intrusion into religion, speech, press, assembly, petition, the right of the people to keep and bear arms (2nd), quartering (3rd), unreasonable searches/seizures (4th), grand jury, double jeopardy, self-incrimination, due process, and takings (5th), criminal and civil jury trials (6th–7th), bail/punishments (8th), unenumerated rights retained by the people (9th), and powers reserved to the States or the people (10th)."
    },
    {
        "id": "bor-washington-farewell-pacificus-helvidius-1793-1796",
        "category": "X. The Bill of Rights, Early Constitutional Practice, Treatises & Dictionaries",
        "title": "Pacificus-Helvidius Debates (1793) & George Washington's Farewell Address (1796)",
        "author": "Alexander Hamilton & James Madison (1793); George Washington, Hamilton, & Madison (1796)",
        "date": "1793 / September 19, 1796",
        "url": "https://avalon.law.yale.edu/18th_century/washing.asp",
        "significance": "Defined the scope of Article II executive foreign-relations power versus Article I war/treaty powers (Pacificus-Helvidius), and delivered Washington's enduring testament that 'Of all the dispositions and habits which lead to political prosperity, religion and morality are indispensable supports,' warning against partisan faction, public debt, usurpation by precedent instead of amendment, and permanent foreign entanglements."
    },
    {
        "id": "bor-kentucky-virginia-resolutions-report-1800",
        "category": "X. The Bill of Rights, Early Constitutional Practice, Treatises & Dictionaries",
        "title": "The Kentucky and Virginia Resolutions (1798–1799) & James Madison's Report of 1800",
        "author": "Thomas Jefferson & James Madison",
        "date": "1798–1800",
        "url": "https://avalon.law.yale.edu/18th_century/virres.asp",
        "significance": "Classic exposition of strict enumerated powers and First Amendment speech/press freedom against the Sedition Act of 1798."
    },
    {
        "id": "bor-founding-dictionaries-johnson-jacob-webster",
        "category": "X. The Bill of Rights, Early Constitutional Practice, Treatises & Dictionaries",
        "title": "Founding-Era Legal & Language Dictionaries: Samuel Johnson's Dictionary (1755), Giles Jacob's New Law-Dictionary (1729/1782), & Noah Webster's American Dictionary (1828)",
        "author": "Samuel Johnson, Giles Jacob, & Noah Webster",
        "date": "1755–1828",
        "url": "https://webstersdictionary1828.com/",
        "significance": "Essential lexical authorities used by textualists and originalists (Scalia, Thomas) to fix the semantic meaning of constitutional terms ('commerce,' 'arms,' 'regulate,' 'establishment,' 'emolument,' 'privilege,' 'due process') at the time of enactment."
    },
    {
        "id": "bor-early-constitutional-treatises-tucker-story-kent-cooley",
        "category": "X. The Bill of Rights, Early Constitutional Practice, Treatises & Dictionaries",
        "title": "Early American Constitutional Treatises: St. George Tucker's View of the Constitution (1803), William Rawle's A View of the Constitution (1825), James Kent's Commentaries on American Law (1826–1830), Joseph Story's Commentaries on the Constitution (1833), & Thomas M. Cooley's Constitutional Limitations (1868)",
        "author": "St. George Tucker, William Rawle, James Kent, Justice Joseph Story, & Judge Thomas M. Cooley",
        "date": "1803–1868",
        "url": "https://lonang.com/library/reference/tucker-blackstone-notes-reference/",
        "significance": "The foundational post-ratification treatises on American constitutional law: Tucker (1803) provided the Jeffersonian strict-constructionist benchmark (calling the Second Amendment 'the true palladium of liberty'), while Story (1833) and Kent (1826) synthesized Marshall Court nationalism and common-law jurisprudence, and Cooley (1868) anchored Fourteenth Amendment original public meaning."
    },
    {
        "id": "bor-founders-online-kurland-lerner-archives",
        "category": "X. The Bill of Rights, Early Constitutional Practice, Treatises & Dictionaries",
        "title": "Founders Online (Papers of Washington, Adams, Jefferson, Madison, Hamilton, Franklin, & Jay) & Kurland and Lerner's The Founders' Constitution (5 Vols.)",
        "author": "National Historical Publications / Philip B. Kurland & Ralph Lerner (eds.)",
        "date": "1606–1836",
        "url": "https://press-pubs.uchicago.edu/founders/",
        "significance": "Over 185,000 searchable primary letters and diary entries of the Founders alongside Kurland & Lerner's clause-by-clause anthology mapping every article and amendment of the U.S. Constitution to its exact philosophical, English common-law, colonial, convention, and early judicial primary sources."
    }
]

def check_url(entry):
    url = entry["url"]
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return entry["id"], url, resp.getcode()
    except urllib.error.HTTPError as e:
        return entry["id"], url, e.code
    except Exception as e:
        return entry["id"], url, str(e)

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    results = list(ex.map(check_url, CANON))

bad = [r for r in results if r[2] != 200]
print(f"Verified {len(results)} URLs; non-200 count: {len(bad)}")
for b in bad:
    print("  BAD:", b)

# Write JSON
(OUT_DIR / "founding-canon.json").write_text(json.dumps({
    "title": "COVENANT & REPUBLIC — Master Canon of the American Founding",
    "updated_at": "2026-10-28",
    "count": len(CANON),
    "entries": CANON
}, indent=2) + "\n")

# Write Markdown
md_lines = [
    "# COVENANT & REPUBLIC — Master Canon of the American Founding",
    "",
    "A primary-source-verified canon of the Biblical covenants, classical republics, English common-law charters, natural-law treatises, colonial compacts, revolutionary pamphlets, convention journals, ratification debates, and early constitutional commentaries that forged the United States Constitution.",
    ""
]
current_cat = None
for e in CANON:
    if e["category"] != current_cat:
        current_cat = e["category"]
        md_lines.append(f"## {current_cat}")
        md_lines.append("")
    md_lines.append(f"- [{e['title']}]({e['url']}), {e['author']} ({e['date']}) — {e['significance']}")
md_lines.append("")
(OUT_DIR / "founding-canon.md").write_text("\n".join(md_lines))

# Build SQLite FTS5 DB
db_path = OUT_DIR / "founding-canon.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS founding_canon_fts")
c.execute("""
    CREATE VIRTUAL TABLE founding_canon_fts USING fts5(
        id, category, title, author, date, url, significance
    )
""")
for e in CANON:
    c.execute(
        "INSERT INTO founding_canon_fts VALUES (?, ?, ?, ?, ?, ?, ?)",
        (e["id"], e["category"], e["title"], e["author"], e["date"], e["url"], e["significance"])
    )
conn.commit()
conn.close()
print("Saved JSON, Markdown, and SQLite FTS5 DB.")
