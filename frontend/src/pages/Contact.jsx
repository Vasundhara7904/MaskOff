const TEAM_MEMBERS = [
  {
    name: "Vasundhara Yande",
    role: "Dataset Annotation & Architecture Engineer",
    description: "Handles dataset labelling and designs the model architecture for YOLOv8 detection pipelines",
    email: "vasu.yande@gmail.com"
  },
  {
    name: "Abdul Rehman Khatib",
    role: "ML Training & Validation Engineer",
    description: "Trains and rigorously tests advanced neural network models for optimal performance",
    email: "akhatib9134@gmail.com"
  },
  {
    name: "Saad Syed",
    role: "Full-Stack Platform Engineer",
    description: "Architects and deploys the complete web platform and infrastructure",
    email: "saddusayed1308@gmail.com"
  }
];

export default function Contact() {
  return (
    <section className="page">
      <article className="contact-layout">

        <section className="team-section">
          <h2>Meet Our Team</h2>
          <p className="team-subtitle">Innovative minds behind MaskOff</p>
          
          <div className="team-grid">
            {TEAM_MEMBERS.map((member) => (
              <div key={member.email} className="team-card">
                <div className="team-header">
                  <h3>{member.name}</h3>
                  <p className="team-role">{member.role}</p>
                </div>
                <p className="team-description">{member.description}</p>
                <a href={`mailto:${member.email}`} className="team-email">
                  {member.email}
                </a>
              </div>
            ))}
          </div>
        </section>
      </article>
    </section>
  );
}
