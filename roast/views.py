from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY =", os.getenv("GEMINI_API_KEY")[:20])
from django.shortcuts import render
from PyPDF2 import PdfReader
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def home(request):
    roast = ""
    language = "English"

    if request.method == "POST":
        language = request.POST.get("language", "English")

        if "resume" in request.FILES:
            pdf = request.FILES["resume"]
            reader = PdfReader(pdf)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            if not text.strip():
                roast = "⚠️ Couldn't read your PDF. Make sure it's a text-based PDF, not a scanned image."
            else:
                LANG_DATA = {
                    "English": {
                        "error": "🏆 The AI judge retired mid-read. Try again in a minute.",
                        "system": "You are a savage, funny resume roaster. Short paragraphs. Every sentence hits. Quote real lines from the resume and destroy them. No headers, no structure, no fluff. 3 to 5 paragraphs max. End with Flame Score: X/10.",
                        "prompt": """Roast this resume in 3 to 5 short paragraphs. No headers. No lists. Just brutal, funny commentary. Quote the worst lines directly and tear them apart. Every sentence should sting. End the last paragraph with Flame Score: X/10 and one verdict sentence.

Resume:
"""
                    },
                    "Malayalam": {
                        "error": "🏆 AI ജഡ്ജ് വായിക്കുന്നതിനിടെ റിട്ടയർ ചെയ്തു. ഒരു മിനിറ്റ് കഴിഞ്ഞ് ശ്രമിക്കൂ.",
                        "system": "നീ ഒരു savage resume roaster ആണ്. ചെറിയ paragraphs. ഓരോ sentence-ഉം hit ആകണം. Resume-ൽ നിന്ന് worst lines quote ചെയ്ത് destroy ചെയ്യുക. Headers, lists, fluff — ഒന്നും വേണ്ട. 3 to 5 paragraphs. അവസാനം Flame Score: X/10. മലയാളത്തിൽ മാത്രം.",
                        "prompt": """ഈ resume 3 മുതൽ 5 വരെ ചെറിയ paragraphs-ൽ roast ചെയ്യുക. Headers വേണ്ട. Lists വേണ്ട. Brutal, funny commentary മാത്രം. Worst lines directly quote ചെയ്ത് tear apart ചെയ്യുക. ഓരോ sentence-ഉം sting ആകണം. അവസാന paragraph-ൽ Flame Score: X/10 ഉം ഒരു verdict sentence-ഉം.

Resume:
"""
                    },
                    "Hindi": {
                        "error": "🏆 AI जज पढ़ते-पढ़ते रिटायर हो गया। एक मिनट बाद फिर कोशिश करें।",
                        "system": "तुम एक savage resume roaster हो। छोटे paragraphs। हर sentence hit करे। Resume की worst lines quote करो और destroy करो। कोई header नहीं, कोई list नहीं, कोई fluff नहीं। 3 से 5 paragraphs। अंत में Flame Score: X/10। केवल हिन्दी में।",
                        "prompt": """इस resume को 3 से 5 छोटे paragraphs में roast करो। कोई header नहीं। कोई list नहीं। बस brutal, funny commentary। Worst lines directly quote करके tear apart करो। हर sentence sting करे। आखिरी paragraph में Flame Score: X/10 और एक verdict sentence।

CV:
"""
                    },
                    "Tamil": {
                        "error": "🏆 AI நீதிபதி படிக்கும் போதே ஓய்வு பெற்றார். ஒரு நிமிடம் கழித்து முயற்சிக்கவும்.",
                        "system": "நீங்கள் ஒரு savage resume roaster. சிறிய paragraphs. ஒவ்வொரு sentence-உம் hit ஆக வேண்டும். Resume-இல் உள்ள worst lines quote செய்து destroy செய்யுங்கள். Headers, lists, fluff — எதுவும் வேண்டாம். 3 முதல் 5 paragraphs. கடைசியில் Flame Score: X/10. தமிழில் மட்டுமே.",
                        "prompt": """இந்த resume-ஐ 3 முதல் 5 சிறிய paragraphs-ல் roast செய்யுங்கள். Headers வேண்டாம். Lists வேண்டாம். Brutal, funny commentary மட்டுமே. Worst lines நேரடியாக quote செய்து tear apart செய்யுங்கள். ஒவ்வொரு sentence-உம் sting ஆக வேண்டும். கடைசி paragraph-ல் Flame Score: X/10 மற்றும் ஒரு verdict sentence.

விண்ணப்பம்:
"""
                    },
                    "Telugu": {
                        "error": "🏆 AI న్యాయమూర్తి చదివేటప్పుడే రిటైర్ అయ్యారు. ఒక నిమిషం తర్వాత మళ్ళీ ప్రయత్నించండి.",
                        "system": "మీరు ఒక savage resume roaster. చిన్న paragraphs. ప్రతి sentence hit అవ్వాలి. Resume లోని worst lines quote చేసి destroy చేయండి. Headers, lists, fluff — ఏదీ వద్దు. 3 నుండి 5 paragraphs. చివరలో Flame Score: X/10. తెలుగులో మాత్రమే.",
                        "prompt": """ఈ resume-ని 3 నుండి 5 చిన్న paragraphs లో roast చేయండి. Headers వద్దు. Lists వద్దు. Brutal, funny commentary మాత్రమే. Worst lines నేరుగా quote చేసి tear apart చేయండి. ప్రతి sentence sting అవ్వాలి. చివరి paragraph లో Flame Score: X/10 మరియు ఒక verdict sentence.

దరఖాస్తు:
"""
                    },
                    "Kannada": {
                        "error": "🏆 AI ನ್ಯಾಯಾಧೀಶರು ಓದುತ್ತಿರುವಾಗಲೇ ನಿವೃತ್ತರಾದರು. ಒಂದು ನಿಮಿಷದ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
                        "system": "ನೀವು ಒಬ್ಬ savage resume roaster. ಚಿಕ್ಕ paragraphs. ಪ್ರತಿ sentence hit ಆಗಬೇಕು. Resume ನಿಂದ worst lines quote ಮಾಡಿ destroy ಮಾಡಿ. Headers, lists, fluff — ಏನೂ ಬೇಡ. 3 ರಿಂದ 5 paragraphs. ಕೊನೆಯಲ್ಲಿ Flame Score: X/10. ಕನ್ನಡದಲ್ಲಿ ಮಾತ್ರ.",
                        "prompt": """ಈ resume-ಅನ್ನು 3 ರಿಂದ 5 ಚಿಕ್ಕ paragraphs ನಲ್ಲಿ roast ಮಾಡಿ. Headers ಬೇಡ. Lists ಬೇಡ. Brutal, funny commentary ಮಾತ್ರ. Worst lines ನೇರವಾಗಿ quote ಮಾಡಿ tear apart ಮಾಡಿ. ಪ್ರತಿ sentence sting ಆಗಬೇಕು. ಕೊನೆಯ paragraph ನಲ್ಲಿ Flame Score: X/10 ಮತ್ತು ಒಂದು verdict sentence.

ಅರ್ಜಿ:
"""
                    },
                    "Spanish": {
                        "error": "🏆 El juez IA se jubiló a mitad de la lectura. Inténtalo en un minuto.",
                        "system": "Eres un savage resume roaster. Párrafos cortos. Cada frase debe doler. Cita las peores líneas del CV y destrúyelas. Sin headers, sin listas, sin relleno. 3 a 5 párrafos. Termina con Flame Score: X/10. Solo en español.",
                        "prompt": """Haz un roast de este currículum en 3 a 5 párrafos cortos. Sin headers. Sin listas. Solo comentarios brutales y graciosos. Cita directamente las peores líneas y destrúyelas. Cada frase debe arder. En el último párrafo, incluye Flame Score: X/10 y una frase veredicto.

Currículum:
"""
                    },
                    "French": {
                        "error": "🏆 Le juge IA a pris sa retraite en cours de lecture. Réessaie dans une minute.",
                        "system": "Tu es un savage roasteur de CV. Paragraphes courts. Chaque phrase doit faire mal. Cite les pires lignes du CV et détruis-les. Pas de titres, pas de listes, pas de remplissage. 3 à 5 paragraphes. Termine avec Flame Score: X/10. Uniquement en français.",
                        "prompt": """Roaste ce CV en 3 à 5 paragraphes courts. Pas de titres. Pas de listes. Juste des commentaires brutaux et drôles. Cite directement les pires lignes et détruis-les. Chaque phrase doit piquer. Dans le dernier paragraphe, inclus Flame Score: X/10 et une phrase verdict.

CV:
"""
                    },
                    "Arabic": {
                        "error": "🏆 القاضي الذكاء الاصطناعي تقاعد في منتصف القراءة. حاول مرة أخرى بعد دقيقة.",
                        "system": "أنت savage في تحميص السير الذاتية. فقرات قصيرة. كل جملة تضرب. اقتبس أسوأ الأسطر ودمرها. بدون عناوين، بدون قوائم، بدون حشو. 3 إلى 5 فقرات. اختم بـ Flame Score: X/10. باللغة العربية فقط.",
                        "prompt": """قم بتحميص هذه السيرة الذاتية في 3 إلى 5 فقرات قصيرة. بدون عناوين. بدون قوائم. فقط تعليقات وحشية ومضحكة. اقتبس أسوأ الأسطر مباشرة ودمرها. كل جملة يجب أن تلسع. في الفقرة الأخيرة، أضف Flame Score: X/10 وجملة حكم واحدة.

السيرة الذاتية:
"""
                    },
                    "German": {
                        "error": "🏆 Der KI-Richter ist beim Lesen in Rente gegangen. Versuch es in einer Minute nochmal.",
                        "system": "Du bist ein savage Lebenslauf-Roaster. Kurze Absätze. Jeder Satz soll treffen. Zitiere die schlimmsten Zeilen und vernichte sie. Keine Überschriften, keine Listen, kein Füllmaterial. 3 bis 5 Absätze. Ende mit Flame Score: X/10. Nur auf Deutsch.",
                        "prompt": """Roaste diesen Lebenslauf in 3 bis 5 kurzen Absätzen. Keine Überschriften. Keine Listen. Nur brutale, witzige Kommentare. Zitiere die schlimmsten Zeilen direkt und reiß sie auseinander. Jeder Satz soll brennen. Im letzten Absatz: Flame Score: X/10 und ein Urteilssatz.

Lebenslauf:
"""
                    },
                    "Japanese": {
                        "error": "🏆 AI審査員は読んでいる途中で引退しました。1分後にもう一度お試しください。",
                        "system": "あなたはsavageな履歴書ローストの達人です。短いパラグラフ。毎文が刺さること。履歴書の最悪の行を引用して破壊する。見出しなし、リストなし、無駄なし。3〜5パラグラフ。最後にFlame Score: X/10。日本語のみ。",
                        "prompt": """この履歴書を3〜5つの短いパラグラフでローストしてください。見出しなし。リストなし。残酷で面白いコメントのみ。最悪の行を直接引用して破壊してください。毎文が痛くなること。最後のパラグラフにFlame Score: X/10と一つの判決文。

履歴書:
"""
                    },
                }

                lang = LANG_DATA.get(language, LANG_DATA["English"])

                try:
                    full_prompt = lang["system"] + "\n\n" + lang["prompt"] + text
                    response = model.generate_content(full_prompt)
                    roast = response.text
                except Exception as e:
                    print("GEMINI ERROR:", e)
                    roast = lang.get("error", str(e))

    return render(request, "index.html", {"roast": roast, "language": language})