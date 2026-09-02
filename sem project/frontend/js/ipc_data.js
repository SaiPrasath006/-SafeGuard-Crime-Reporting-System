const IPC_MAPPING = {
    "Theft": { section: "IPC Section 378", desc: "Theft is defined as the dishonest removal of movable property." },
    "Assault": { section: "IPC Section 351", desc: "Assault involves any gesture or preparation causing apprehension of force." },
    "Cybercrime": { section: "IT Act 2000", desc: "Covers various digital offenses including hacking and identities theft." },
    "Fraud": { section: "IPC Section 420", desc: "Cheating and dishonestly inducing delivery of property." },
    "Harassment": { section: "IPC Section 354", desc: "Assault or criminal force to woman with intent to outrage her modesty." },
    "Other": { section: "General IPC", desc: "Various sections may apply based on the nature of the crime." }
};

function updateIPCInfo(category) {
    const info = IPC_MAPPING[category];
    const display = document.getElementById('ipc-suggestion');
    if (display && info) {
        display.innerHTML = `
            <div style="background: rgba(0, 0, 128, 0.1); border-left: 4px solid var(--accent); padding: 1rem; margin-top: 1rem; border-radius: 0 0.5rem 0.5rem 0;">
                <p style="color: var(--text-white); font-weight: 700;">Suggested Legal Reference: ${info.section}</p>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.3rem;">${info.desc}</p>
            </div>
        `;
    }
}
