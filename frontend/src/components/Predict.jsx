import React, { useState } from 'react';
import api from '../api';

const ALL_SYMPTOMS =new Set([
    "anxiety and nervousness", "depression", "shortness of breath", "depressive or psychotic symptoms",
    "sharp chest pain", "dizziness", "insomnia", "abnormal involuntary movements", "chest tightness",
    "palpitations", "irregular heartbeat", "breathing fast", "hoarse voice", "sore throat",
    "difficulty speaking", "cough", "nasal congestion", "throat swelling", "diminished hearing",
    "lump in throat", "throat feels tight", "difficulty in swallowing", "skin swelling", "retention of urine",
    "groin mass", "leg pain", "hip pain", "suprapubic pain", "blood in stool",
    "lack of growth", "emotional symptoms", "elbow weakness", "back weakness", "pus in sputum",
    "symptoms of the scrotum and testes", "swelling of scrotum", "pain in testicles", "flatulence", "pus draining from ear",
    "jaundice", "mass in scrotum", "white discharge from eye", "irritable infant", "abusing alcohol",
    "fainting", "hostile behavior", "drug abuse", "sharp abdominal pain", "feeling ill",
    "vomiting", "headache", "nausea", "diarrhea", "vaginal itching",
    "vaginal dryness", "painful urination", "involuntary urination", "pain during intercourse", "frequent urination",
    "lower abdominal pain", "vaginal discharge", "blood in urine", "hot flashes", "intermenstrual bleeding",
    "hand or finger pain", "wrist pain", "hand or finger swelling", "arm pain", "wrist swelling",
    "arm stiffness or tightness", "arm swelling", "hand or finger stiffness or tightness", "wrist stiffness or tightness", "lip swelling",
    "toothache", "abnormal appearing skin", "skin lesion", "acne or pimples", "dry lips",
    "facial pain", "mouth ulcer", "skin growth", "eye deviation", "diminished vision",
    "double vision", "cross-eyed", "symptoms of eye", "pain in eye", "eye moves abnormally",
    "abnormal movement of eyelid", "foreign body sensation in eye", "irregular appearing scalp", "swollen lymph nodes", "back pain",
    "neck pain", "low back pain", "pain of the anus", "pain during pregnancy", "pelvic pain",
    "impotence", "infant spitting up", "vomiting blood", "regurgitation", "burning abdominal pain",
    "restlessness", "symptoms of infants", "wheezing", "peripheral edema", "neck mass",
    "ear pain", "jaw swelling", "mouth dryness", "neck swelling", "knee pain",
    "foot or toe pain", "bowlegged or knock-kneed", "ankle pain", "bones are painful", "knee weakness",
    "elbow pain", "knee swelling", "skin moles", "knee lump or mass", "weight gain",
    "problems with movement", "knee stiffness or tightness", "leg swelling", "foot or toe swelling", "heartburn",
    "smoking problems", "muscle pain", "infant feeding problem", "recent weight loss", "problems with shape or size of breast",
    "underweight", "difficulty eating", "scanty menstrual flow", "vaginal pain", "vaginal redness",
    "vulvar irritation", "weakness", "decreased heart rate", "increased heart rate", "bleeding or discharge from nipple",
    "ringing in ear", "plugged feeling in ear", "itchy ear(s)", "frontal headache", "fluid in ear",
    "neck stiffness or tightness", "spots or clouds in vision", "eye redness", "lacrimation", "itchiness of eye",
    "blindness", "eye burns or stings", "itchy eyelid", "feeling cold", "decreased appetite",
    "excessive appetite", "excessive anger", "loss of sensation", "focal weakness", "slurring words",
    "symptoms of the face", "disturbance of memory", "paresthesia", "side pain", "fever",
    "shoulder pain", "shoulder stiffness or tightness", "shoulder weakness", "arm cramps or spasms", "shoulder swelling",
    "tongue lesions", "leg cramps or spasms", "abnormal appearing tongue", "ache all over", "lower body pain",
    "problems during pregnancy", "spotting or bleeding during pregnancy", "cramps and spasms", "upper abdominal pain", "stomach bloating",
    "changes in stool appearance", "unusual color or odor to urine", "kidney mass", "swollen abdomen", "symptoms of prostate",
    "leg stiffness or tightness", "difficulty breathing", "rib pain", "joint pain", "muscle stiffness or tightness",
    "pallor", "hand or finger lump or mass", "chills", "groin pain", "fatigue",
    "abdominal distention", "regurgitation", "symptoms of the kidneys", "melena", "flushing",
    "coughing up sputum", "seizures", "delusions or hallucinations", "shoulder cramps or spasms", "joint stiffness or tightness",
    "pain or soreness of breast", "excessive urination at night", "bleeding from eye", "rectal bleeding", "constipation",
    "temper problems", "coryza", "wrist weakness", "eye strain", "hemoptysis",
    "lymphedema", "skin on leg or foot looks infected", "allergic reaction", "congestion in chest", "muscle swelling",
    "pus in urine", "abnormal size or shape of ear", "low back weakness", "sleepiness", "apnea",
    "abnormal breathing sounds", "excessive growth", "elbow cramps or spasms", "feeling hot and cold", "blood clots during menstrual periods",
    "absence of menstruation", "pulling at ears", "gum pain", "redness in ear", "fluid retention",
    "flu-like syndrome", "sinus congestion", "painful sinuses", "fears and phobias", "recent pregnancy",
    "uterine contractions", "burning chest pain", "back cramps or spasms", "stiffness all over", "muscle cramps, contractures, or spasms",
    "low back cramps or spasms", "back mass or lump", "nosebleed", "long menstrual periods", "heavy menstrual flow",
    "unpredictable menstruation", "painful menstruation", "infertility", "frequent menstruation", "sweating",
    "mass on eyelid", "swollen eye", "eyelid swelling", "eyelid lesion or rash", "unwanted hair",
    "symptoms of bladder", "irregular appearing nails", "itching of skin", "hurts to breath", "nailbiting",
    "skin dryness, peeling, scaliness, or roughness", "skin on arm or hand looks infected", "skin irritation", "itchy scalp", "hip swelling",
    "incontinence of stool", "foot or toe cramps or spasms", "warts", "bumps on penis", "too little hair",
    "foot or toe lump or mass", "skin rash", "mass or swelling around the anus", "low back swelling", "ankle swelling",
    "hip lump or mass", "drainage in throat", "dry or flaky scalp", "premenstrual tension or irritability", "feeling hot",
    "feet turned in", "foot or toe stiffness or tightness", "pelvic pressure", "elbow swelling", "elbow stiffness or tightness",
    "early or late onset of menopause", "mass on ear", "bleeding from ear", "hand or finger weakness", "low self-esteem",
    "throat irritation", "itching of the anus", "swollen or red tonsils", "irregular belly button", "swollen tongue",
    "lip sore", "vulvar sore", "hip stiffness or tightness", "mouth pain", "arm weakness",
    "leg lump or mass", "disturbance of smell or taste", "discharge in stools", "penis pain", "loss of sex drive",
    "obsessions and compulsions", "antisocial behavior", "neck cramps or spasms", "pupils unequal", "poor circulation",
    "thirst", "sleepwalking", "skin oiliness", "sneezing", "bladder mass",
    "knee cramps or spasms", "premature ejaculation", "leg weakness", "posture problems", "bleeding in mouth",
    "tongue bleeding", "change in skin mole size or color", "penis redness", "penile discharge", "shoulder lump or mass",
    "polyuria", "cloudy eye", "hysterical behavior", "arm lump or mass", "nightmares",
    "bleeding gums", "pain in gums", "bedwetting", "diaper rash", "lump or mass of breast",
    "vaginal bleeding after menopause", "infrequent menstruation", "mass on vulva", "jaw pain", "itching of scrotum",
    "postpartum problems of the breast", "eyelid retracted", "hesitancy", "elbow lump or mass", "muscle weakness",
    "throat redness", "joint swelling", "tongue pain", "redness in or around nose", "wrinkles on skin",
    "foot or toe weakness", "hand or finger cramps or spasms", "back stiffness or tightness", "wrist lump or mass", "skin pain",
    "low back stiffness or tightness", "low urine output", "skin on head or neck looks infected", "stuttering or stammering", "problems with orgasm",
    "nose deformity", "lump over jaw", "sore in nose", "hip weakness", "back swelling",
    "ankle stiffness or tightness", "ankle weakness", "neck weakness"
]);

const Predict = () => {
    const [search, setSearch] = useState('');
    const [selected, setSelected] = useState({});
    const [description, setDescription] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const toggleSymptom = (symptom) => {
        setSelected(prev => {
            const newState = { ...prev };
            if (newState[symptom]) {
                delete newState[symptom];
            } else {
                newState[symptom] = 1;
            }
            return newState;
        });
    };

    const handlePredict = async () => {
        setLoading(true);
        try {

            const selectedKeys = Object.keys(selected);
            const payload = {
                amount: selectedKeys.length,
                description: description || "No description provided",
            };

            selectedKeys.forEach((symptom, index) => {
                payload[index] = symptom;
            });

            const response = await api.post('/disease/predict', payload);

            setResult(`Disease record created successfully! It's a ${response.data.message}`);

        } catch (err) {
            console.error(err);
            setResult("Error processing prediction.");
        } finally {
            setLoading(false);
        }
    };

    const filteredSymptoms = Array.from(ALL_SYMPTOMS).filter(s =>
        s.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-bold mb-4">Select Symptoms</h2>
                <input
                    type="text"
                    placeholder="Search symptoms..."
                    className="w-full p-3 border rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    onChange={(e) => setSearch(e.target.value)}
                />

                <div className="h-64 overflow-y-auto border p-2 rounded grid grid-cols-2 md:grid-cols-3 gap-2 bg-gray-50">
                    {filteredSymptoms.map((s) => (
                        <div
                            key={s}
                            onClick={() => toggleSymptom(s)}
                            className={`cursor-pointer p-2 text-sm rounded border transition-all ${
                                selected[s] ? 'bg-blue-500 text-white border-blue-600 shadow-sm' : 'bg-white hover:bg-gray-100'
                            }`}
                        >
                            {s}
                        </div>
                    ))}
                </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="font-bold mb-2">Case Description</h3>
                <div className="relative mb-6">
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        maxLength={100}
                        rows="3"
                        placeholder="Describe the case briefly (max 100 characters)..."
                        className="w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-green-400 resize-none"
                    />
                    <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                        {description.length} / 100
                    </div>
                </div>

                <h3 className="font-bold mb-2">Selected Symptoms ({Object.keys(selected).length})</h3>
                <div className="flex flex-wrap gap-2 mb-6">
                    {Object.keys(selected).length > 0 ? (
                        Object.keys(selected).map(s => (
                            <span key={s} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">
                                {s}
                            </span>
                        ))
                    ) : (
                        <span className="text-gray-400 italic text-sm">No symptoms selected yet.</span>
                    )}
                </div>

                <button
                    onClick={handlePredict}
                    disabled={loading || Object.keys(selected).length === 0}
                    className="w-full bg-green-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {loading ? 'Analyzing...' : 'Predict & Save Report'}
                </button>

                {result && (
                    <div className={`mt-4 p-4 rounded border ${result.includes('Error') ? 'bg-red-50 border-red-200 text-red-800' : 'bg-green-50 border-green-200 text-green-800'}`}>
                        {result}
                    </div>
                )}
            </div>
        </div>
    );
};
export default Predict;