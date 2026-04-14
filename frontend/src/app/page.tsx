"use client";

//import sections
import { useState, useEffect , useRef} from "react";
import { useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";

export default function Home() {

  
  const router = useRouter();//login check ke liye

  //state variables[app ka data store]

  const [code, setCode] = useState(""); // user ka input code
  const [repoUrl, setRepoUrl] = useState("");  // GitHub repo URL
  const [result, setResult] = useState<any>(null); // backend se response
  const [loading, setLoading] = useState(false); //// loading state
  const [tab, setTab] = useState("analysis"); // UI tab control
  const [language, setLanguage] = useState("en");  // language toggle (EN/HI)
  const recognitionRef = useRef<any>(null);  //// speech recognition ref (future use)
  const [streamText, setStreamText] = useState("");     // streaming text
  const [translatedStream, setTranslatedStream] = useState(""); // translated text

  //login check (agar login nhi hai to redirect)
  useEffect(() => {
    if (!localStorage.getItem("isLoggedIn")) {
      router.replace("/login");
    }
  }, []);



  //  Translate
  const translateText = async (text: string, target = "hi") => {
    try {
      const res = await fetch(
        `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${target}&dt=t&q=${encodeURIComponent(
          text
        )}`
      );
      const data = await res.json();
      return data[0].map((t: any) => t[0]).join("");
    } catch {
      return text;
    }
  };
//  STREAM RESPONSE FUNCTION
//(Text ko word-by-word show karta hai)
  const streamResponse = async (fullText: string) => {
    let words = fullText.split(" ");
  
    setStreamText("");
    setTranslatedStream("");
  
    window.speechSynthesis.cancel();
  
    for (let i = 0; i < words.length; i++) {
      await new Promise((res) => setTimeout(res, 35));
  
      const current = words.slice(0, i + 1).join(" ");
      setStreamText(current);
  
      if (language === "hi") {
        const translated = await translateText(current, "hi");
        setTranslatedStream(translated);
      } else {
        setTranslatedStream(current);
      }
    }
  
    //  SPEAK ONLY ONCE AFTER COMPLETE
    //currently in progress
    const finalText =
      language === "hi"
        ? await translateText(fullText, "hi")
        : fullText;
  
    if (!finalText) return;
    setTimeout(() => {
    }, 300);
  };

 /**
   REVIEW CODE FUNCTION
  (User code backend pe bhejta hai)
  */
  const reviewCode = async () => {
    if (!code) return alert("Enter code first");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      const data = await res.json();
      setResult(data);  // result store
      streamResponse(data.analysis); // streaming start
    } catch {
      alert("Server error");
    }

    setLoading(false);
  };

  /*
  ANALYZE REPOSITORY FUNCTION
  (GitHub repo analyze karta hai)
  */
  const analyzeRepo = async () => {
    if (!repoUrl) return alert("Enter repo URL");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/repo-review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      const data = await res.json();
      setResult(data);
      streamResponse(data.analysis);
    } catch {
      alert("Repo analysis failed");
    }

    setLoading(false);
  };

  // useEffect(() => {
  //   if (translatedStream) speak(translatedStream);
  // }, [translatedStream]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#020617] via-[#020617] to-[#0f172a] text-white">

      {/* 🔥 Glow background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(168,85,247,0.15),transparent)]"></div>

      {/* LOGOUT */}
      <button
        onClick={() => {
          localStorage.removeItem("isLoggedIn");
          router.replace("/login");
        }}
        className="absolute top-6 right-6 bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg shadow-lg"
      >
        Logout
      </button>

      <div className="max-w-7xl mx-auto p-6 relative z-10">

        {/* HEADER */}
<h1 className="text-center text-6xl md:text-7xl font-extrabold mb-12 tracking-wide relative">

  <span className="relative z-10 text-transparent bg-clip-text bg-gradient-to-r from-pink-400 via-purple-500 to-indigo-500 
  drop-shadow-[0_5px_15px_rgba(168,85,247,0.8)]">
    AI CODE REVIEW AGENT
  </span>

</h1>

        {/* Language */}
        <div className="flex justify-center gap-3 mb-10">
          {["en", "hi"].map((lang) => (
            <button
              key={lang}
              onClick={() => setLanguage(lang)}
              className={`px-5 py-1.5 rounded-full transition-all ${
                language === lang
                  ? "bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg"
                  : "bg-white/10 hover:bg-white/20"
              }`}
            >
              {lang === "en" ? "English" : "हिंदी"}
            </button>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-8">

          {/* LEFT */}
          <div className="bg-white/5 backdrop-blur-2xl p-6 rounded-3xl border border-white/10 shadow-2xl hover:shadow-purple-500/10 transition">

            <input
              placeholder="🔗 Enter GitHub Repo URL..."
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              className="w-full p-3 mb-4 bg-black/70 rounded-xl border border-white/10 focus:ring-2 focus:ring-purple-500 outline-none"
            />

            <button
              onClick={analyzeRepo}
              className="w-full mb-5 py-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-xl hover:scale-105 transition shadow-lg"
            >
               Analyze GitHub Repo
            </button>

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="💻 Paste your code here..."
              className="w-full h-72 bg-black text-green-400 p-4 rounded-xl border border-white/10 font-mono text-sm"
            />


            <button
              onClick={reviewCode}
              className="w-full mt-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-lg font-semibold shadow-lg hover:scale-105 transition"
            >
              {loading ? "Analyzing..." : " Review Code"}
            </button>
          </div>

          {/* RIGHT */}
          <div className="bg-gradient-to-br from-[#0f172a] to-[#020617] p-6 rounded-3xl border border-white/10 shadow-2xl">

            {!result ? (
              <div className="flex items-center justify-center h-full text-gray-400">
                No analysis available
              </div>
            ) : (
              <>
                {/* SCORE BOX */}
                <div className="flex justify-between mb-5">
                  <h2 className="text-xl font-semibold">Report</h2>

                  <div className="text-right space-y-1">
                    <div className="text-yellow-400 font-semibold">
                      Score: {result?.score ?? "N/A"}
                    </div>
<span className="px-2 py-0.5 rounded text-xs bg-blue-500/20 text-blue-300">
  Complexity: {result?.complexity || "N/A"}
</span>
<br></br>
<span className="px-2 py-0.5 rounded text-xs bg-green-500/20 text-green-300">
  Label: {result?.label || "N/A"}
</span>
                  </div>
                </div>

                {/* TABS */}
                <div className="flex gap-2 mb-4">
                  {["analysis", "issues", "fix", "report"].map((t) => (
                    <button
                      key={t}
                      onClick={() => setTab(t)}
                      className={`px-4 py-1.5 rounded-full text-sm ${
                        tab === t
                          ? "bg-gradient-to-r from-purple-500 to-pink-500"
                          : "bg-white/5 hover:bg-white/10"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>

                {/* CONTENT */}
                <div className="bg-black/40 p-4 rounded-xl max-h-[500px] overflow-y-auto text-sm">
                  {tab === "analysis" && (
                    <>
                      {streamText}
                      <span className="animate-pulse">|</span>
                      {language === "hi" && (
                        <div className="text-green-400 mt-3 border-t pt-2">
                          {translatedStream}
                        </div>
                      )}
                    </>
                  )}

                  {tab === "issues" &&
                    result.issues?.map((i: string, idx: number) => (
                      <p key={idx}>• {i}</p>
                    ))}

                  {tab === "fix" && <pre>{result.fixed_code}</pre>}

                  {tab === "report" && (
                    <ReactMarkdown>{result.report}</ReactMarkdown>
                  )}
                </div>
              </>
            )}
          </div>
        </div>

        {/*  FOOTER */}
        <footer className="mt-16 text-center text-gray-400">
          <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-purple-500 to-transparent mb-6"></div>
          <p> AI Code Review Agent</p>
          <p className="text-xs mt-2">Analyze • Detect • Fix • Optimize</p>
          <p className="text-xs mt-1">© {new Date().getFullYear()} Harsh Kumar Mandal </p>
        </footer>

      </div>
    </main>
  );
}


