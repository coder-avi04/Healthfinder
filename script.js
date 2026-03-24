// 🔥 Bhilai Doctors Data (Real-style)
const doctors = [
  {
    name: "Dr. R.K. Jain",
    spec: "Cardiologist",
    city: "Bhilai",
    symptoms: ["chest pain","heart","bp"],
    phone: "9876543210",
    img: "https://randomuser.me/api/portraits/men/32.jpg"
  },
  {
    name: "Dr. Neha Jain",
    spec: "Dermatologist",
    city: "Bhilai",
    symptoms: ["skin","pimples","hair fall"],
    phone: "9123456780",
    img: "https://randomuser.me/api/portraits/women/44.jpg"
  },
  {
    name: "Dr. Vivek Sharma",
    spec: "General Physician",
    city: "Bhilai",
    symptoms: ["fever","cold","cough"],
    phone: "9012345678",
    img: "https://randomuser.me/api/portraits/men/55.jpg"
  },
  {
    name: "Dr. Sanjay Tiwari",
    spec: "Cardiologist",
    city: "Bhilai",
    symptoms: ["heart","bp"],
    phone: "9988776655",
    img: "https://randomuser.me/api/portraits/men/60.jpg"
  },
  {
    name: "Dr. Ritu Agrawal",
    spec: "Dermatologist",
    city: "Bhilai",
    symptoms: ["skin","allergy"],
    phone: "9090909090",
    img: "https://randomuser.me/api/portraits/women/68.jpg"
  }
];

// Add more doctors (auto generate)
for(let i=6;i<=25;i++){
  doctors.push({
    name: "Dr. Bhilai "+i,
    spec: "Specialist",
    city: "Bhilai",
    symptoms: ["general"],
    phone: "9"+Math.floor(Math.random()*1000000000),
    img: "https://randomuser.me/api/portraits/men/"+i+".jpg"
  });
}

const container = document.getElementById("doctorList");

// 🔥 Show Doctors
function displayDoctors(list){
  container.innerHTML="";
  list.forEach(doc=>{
    container.innerHTML += `
      <div class="card">
        <img src="${doc.img}">
        <h3>${doc.name}</h3>
        <p>${doc.spec}</p>
        <p>📞 ${doc.phone}</p>
        <button onclick="alert('Booked ${doc.name}')">Book Now</button>
      </div>
    `;
  });
}
// Scroll to doctors
function scrollToDoctors(){
  document.getElementById("doctors").scrollIntoView({behavior:"smooth"});
}

// Load all
displayDoctors(doctors);

// 🔍 Search by Symptoms
function searchDoctors(){
  let input = document.querySelector(".hero input").value.toLowerCase();

  let filtered = doctors.filter(doc =>
    doc.symptoms.some(s => s.includes(input))
  );

  displayDoctors(filtered);
}