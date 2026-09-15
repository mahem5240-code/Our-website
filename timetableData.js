// Source of truth: Trinity College of Engineering & Technology, Peddapalli-505172
// Department of AIML — W.E.F. 06-JULY-2026
// Transcribed from the official department timetable. Where a printed cell was
// a merged lab block spanning a break, it is represented as one entry with the
// full start/end time it visually covers.

export const PERIODS = [
  { id: 'p1', start: '09:30', end: '10:20', label: '9:30 – 10:20 AM' },
  { id: 'p2', start: '10:20', end: '11:10', label: '10:20 – 11:10 AM' },
  { id: 'break', start: '11:10', end: '11:20', label: '11:10 – 11:20 AM', kind: 'break' },
  { id: 'p3', start: '11:20', end: '12:10', label: '11:20 AM – 12:10 PM' },
  { id: 'p4', start: '12:10', end: '13:00', label: '12:10 – 1:00 PM' },
  { id: 'lunch', start: '13:00', end: '13:45', label: '1:00 – 1:45 PM', kind: 'lunch' },
  { id: 'p5', start: '13:45', end: '14:30', label: '1:45 – 2:30 PM' },
  { id: 'p6', start: '14:30', end: '15:15', label: '2:30 – 3:15 PM' },
  { id: 'p7', start: '15:15', end: '16:00', label: '3:15 – 4:00 PM' },
]

export const DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
export const DAY_LABELS = {
  MON: 'Monday', TUE: 'Tuesday', WED: 'Wednesday',
  THU: 'Thursday', FRI: 'Friday', SAT: 'Saturday',
}

// entry: { start, end, code, type: 'lecture'|'lab'|'special', room? }
// codes resolve against each year's `subjects` map for name/faculty/color.

export const YEARS = {
  y2: {
    id: 'y2',
    label: '2nd Year',
    sem: 'AIML B.Tech II Year · I Sem',
    incharge: 'Mrs. Tarannum Fatima',
    accent: 'blue',
    subjects: {
      DBMS: { name: 'Database Management Systems', faculty: 'Syed. Khaja Pasha', color: 'blue' },
      MSF: { name: 'Mathematical & Statistical Foundations', faculty: 'Mrs. K. Naga Laxmi', color: 'indigo' },
      OOPJ: { name: 'Object Oriented Programming (Java)', faculty: 'G. Lakshmi', color: 'teal' },
      COA: { name: 'Computer Organization & Architecture', faculty: 'Tarannum Fatima', color: 'orange' },
      SE: { name: 'Software Engineering', faculty: 'P. Lavanya', color: 'purple' },
      'DBMS LAB': { name: 'DBMS Lab', faculty: 'Syed. Khaja Pasha', color: 'blue', isLab: true },
      'SE LAB': { name: 'Software Engineering Lab', faculty: 'P. Lavanya', color: 'purple', isLab: true },
      'NODEJS LAB': { name: 'Node.js Lab', faculty: 'G. Lakshmi', color: 'teal', isLab: true },
      'OOPJ LAB': { name: 'OOP (Java) Lab', faculty: 'G. Lakshmi', color: 'teal', isLab: true },
      'CM LAB': { name: 'Computational Methods Lab', faculty: 'Dr. Mani Ganesh', color: 'pink', isLab: true },
    },
    schedule: {
      MON: [
        { start: '09:30', end: '10:20', code: 'DBMS' },
        { start: '10:20', end: '13:00', code: 'OOPJ LAB', type: 'lab' },
        { start: '13:45', end: '14:30', code: 'SE' },
        { start: '14:30', end: '15:15', code: 'OOPJ' },
        { start: '15:15', end: '16:00', code: 'MSF' },
      ],
      TUE: [
        { start: '09:30', end: '10:20', code: 'MSF' },
        { start: '10:20', end: '13:00', code: 'NODEJS LAB', type: 'lab' },
        { start: '13:45', end: '14:30', code: 'SE' },
        { start: '14:30', end: '15:15', code: 'COA' },
        { start: '15:15', end: '16:00', code: 'DBMS' },
      ],
      WED: [
        { start: '09:30', end: '10:20', code: 'OOPJ' },
        { start: '10:20', end: '11:10', code: 'MSF' },
        { start: '11:20', end: '12:10', code: 'COA' },
        { start: '12:10', end: '13:00', code: 'COA' },
        { start: '13:45', end: '14:30', code: 'SE' },
        { start: '14:30', end: '15:15', code: 'SE' },
        { start: '15:15', end: '16:00', code: 'OOPJ' },
      ],
      THU: [
        { start: '09:30', end: '10:20', code: 'COA' },
        { start: '10:20', end: '11:10', code: 'OOPJ' },
        { start: '11:20', end: '12:10', code: 'OOPJ' },
        { start: '12:10', end: '13:00', code: 'DBMS' },
        { start: '13:45', end: '16:00', code: 'CM LAB', type: 'lab' },
      ],
      FRI: [
        { start: '09:30', end: '10:20', code: 'MSF' },
        { start: '10:20', end: '13:00', code: 'DBMS LAB', type: 'lab' },
        { start: '13:45', end: '14:30', code: 'COA' },
        { start: '14:30', end: '15:15', code: 'DBMS' },
        { start: '15:15', end: '16:00', code: 'MSF' },
      ],
      SAT: [
        { start: '09:30', end: '10:20', code: 'DBMS' },
        { start: '10:20', end: '13:00', code: 'SE LAB', type: 'lab' },
        { start: '13:45', end: '14:30', code: 'MSF' },
        { start: '14:30', end: '15:15', code: 'SE' },
        { start: '15:15', end: '16:00', code: 'COA' },
      ],
    },
  },

  y3: {
    id: 'y3',
    label: '3rd Year',
    sem: 'AIML B.Tech III Year · I Sem',
    incharge: 'Mrs. P. Lavanya',
    accent: 'indigo',
    subjects: {
      DAA: { name: 'Design & Analysis of Algorithms', faculty: 'Tarannum Fatima', color: 'blue' },
      ML: { name: 'Machine Learning', faculty: 'G. Vidyasagar', color: 'purple' },
      CN: { name: 'Computer Networks', faculty: 'P. Lavanya', color: 'orange' },
      BEFA: { name: 'Business Economics & Financial Analysis', faculty: 'Dr. Arif Arfath', color: 'teal' },
      WP: { name: 'Web Programming', faculty: 'SD. Khaja Pasha', color: 'pink' },
      FLUTTER: { name: 'Flutter Skill Session', faculty: 'Department Faculty', color: 'green', isLab: true },
      'ML LAB': { name: 'Machine Learning Lab', faculty: 'G. Vidyasagar', color: 'purple', isLab: true },
      'AECS LAB': { name: 'AECS Lab', faculty: 'B. Raju', color: 'indigo', isLab: true },
      'CN LAB': { name: 'Computer Networks Lab', faculty: 'P. Lavanya', color: 'orange', isLab: true },
    },
    schedule: {
      MON: [
        { start: '09:30', end: '10:20', code: 'DAA' },
        { start: '10:20', end: '11:10', code: 'ML' },
        { start: '11:20', end: '12:10', code: 'CN' },
        { start: '12:10', end: '13:00', code: 'WP' },
        { start: '13:45', end: '14:30', code: 'ML' },
        { start: '14:30', end: '15:15', code: 'BEFA' },
        { start: '15:15', end: '16:00', code: 'WP' },
      ],
      TUE: [
        { start: '09:30', end: '10:20', code: 'DAA' },
        { start: '10:20', end: '11:10', code: 'WP' },
        { start: '11:20', end: '12:10', code: 'CN' },
        { start: '12:10', end: '13:00', code: 'ML' },
        { start: '13:45', end: '16:00', code: 'ML LAB', type: 'lab' },
      ],
      WED: [
        { start: '09:30', end: '10:20', code: 'DAA' },
        { start: '10:20', end: '11:10', code: 'ML' },
        { start: '11:20', end: '12:10', code: 'WP' },
        { start: '12:10', end: '13:00', code: 'CN' },
        { start: '13:45', end: '16:00', code: 'AECS LAB', type: 'lab' },
      ],
      THU: [
        { start: '09:30', end: '10:20', code: 'WP' },
        { start: '10:20', end: '12:10', code: 'FLUTTER', type: 'lab' },
        { start: '12:10', end: '13:00', code: 'CN' },
        { start: '13:45', end: '16:00', code: 'CN LAB', type: 'lab' },
      ],
      FRI: [
        { start: '09:30', end: '10:20', code: 'DAA' },
        { start: '10:20', end: '11:10', code: 'BEFA' },
        { start: '11:20', end: '12:10', code: 'CN' },
        { start: '12:10', end: '13:00', code: 'WP' },
        { start: '13:45', end: '14:30', code: 'CN' },
        { start: '14:30', end: '15:15', code: 'BEFA' },
        { start: '15:15', end: '16:00', code: 'ML' },
      ],
      SAT: [
        { start: '09:30', end: '10:20', code: 'CN' },
        { start: '10:20', end: '11:10', code: 'ML' },
        { start: '11:20', end: '12:10', code: 'WP' },
        { start: '12:10', end: '13:00', code: 'DAA' },
        { start: '13:45', end: '14:30', code: 'CN' },
        { start: '14:30', end: '15:15', code: 'BEFA' },
        { start: '15:15', end: '16:00', code: 'ML' },
      ],
    },
  },

  y4: {
    id: 'y4',
    label: '4th Year',
    sem: 'AIML B.Tech IV Year · I Sem',
    incharge: 'Mr. SD. Khaja Pasha',
    accent: 'orange',
    subjects: {
      DL: { name: 'Deep Learning', faculty: 'G. Lakshmi', color: 'blue' },
      NIC: { name: 'Nature Inspired Computing', faculty: 'K. Ashok', color: 'indigo' },
      CC: { name: 'Cloud Computing', faculty: 'P. Lavanya', color: 'purple' },
      SW: { name: 'Semantic Web', faculty: 'SD. Khaja Pasha', color: 'pink' },
      DM: { name: 'Data Mining', faculty: 'Tarannum Fatima', color: 'orange' },
      PPLE: { name: 'Professional & Personality Development', faculty: 'Department Faculty', color: 'teal' },
      'CC LAB': { name: 'Cloud Computing Lab', faculty: 'P. Lavanya', color: 'purple', isLab: true },
      'PROJECT STAGE-I': { name: 'Project Stage – I', faculty: 'Project Guides', color: 'green', isLab: true },
      SOFTSKILLS: { name: 'Soft Skills', faculty: 'G. Lakshmi & SD. Khaja Pasha', color: 'teal', isLab: true },
    },
    schedule: {
      MON: [
        { start: '09:30', end: '10:20', code: 'CC' },
        { start: '10:20', end: '11:10', code: 'NIC' },
        { start: '11:20', end: '12:10', code: 'DM' },
        { start: '12:10', end: '13:00', code: 'DM' },
        { start: '13:45', end: '14:30', code: 'DL' },
        { start: '14:30', end: '15:15', code: 'CC' },
        { start: '15:15', end: '16:00', code: 'PPLE' },
      ],
      TUE: [
        { start: '09:30', end: '10:20', code: 'CC' },
        { start: '10:20', end: '11:10', code: 'NIC' },
        { start: '11:20', end: '12:10', code: 'NIC' },
        { start: '12:10', end: '13:00', code: 'SW' },
        { start: '13:45', end: '14:30', code: 'DM' },
        { start: '14:30', end: '15:15', code: 'DL' },
        { start: '15:15', end: '16:00', code: 'PPLE' },
      ],
      WED: [
        { start: '09:30', end: '10:20', code: 'CC' },
        { start: '10:20', end: '12:10', code: 'CC LAB', type: 'lab' },
        { start: '13:45', end: '14:30', code: 'SW' },
        { start: '14:30', end: '15:15', code: 'SW' },
        { start: '15:15', end: '16:00', code: 'PPLE' },
      ],
      THU: [
        { start: '09:30', end: '10:20', code: 'CC' },
        { start: '10:20', end: '11:10', code: 'NIC' },
        { start: '11:20', end: '12:10', code: 'DM' },
        { start: '12:10', end: '13:00', code: 'DL' },
        { start: '13:45', end: '15:15', code: 'PROJECT STAGE-I', type: 'lab' },
        { start: '15:15', end: '16:00', code: 'PPLE' },
      ],
      FRI: [
        { start: '09:30', end: '10:20', code: 'CC' },
        { start: '10:20', end: '11:10', code: 'NIC' },
        { start: '11:20', end: '12:10', code: 'DM' },
        { start: '12:10', end: '13:00', code: 'DL' },
        { start: '13:45', end: '15:15', code: 'SOFTSKILLS', type: 'lab' },
        { start: '15:15', end: '16:00', code: 'PPLE' },
      ],
      SAT: [
        { start: '09:30', end: '10:20', code: 'DL' },
        { start: '10:20', end: '11:10', code: 'NIC' },
        { start: '11:20', end: '12:10', code: 'DM' },
        { start: '12:10', end: '13:00', code: 'SW' },
      ],
    },
  },
}

export const YEAR_ORDER = ['y2', 'y3', 'y4']
