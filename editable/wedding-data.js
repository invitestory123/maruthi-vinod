/**
 * wedding-data.js — Customer-facing editable data layer for kalyana-mandapam
 * Edit this file to update couple names, Telugu text, families, dates, venue, and images.
 */

window.WEDDING_DATA = {
  couple: {
    bride: "Maruthi",
    groom: "Vinod",
    hashtag: "#MaruthiWedsVinod",
    brideFamily: "The Maruthi Family",
    groomFamily: "The Vinod Family",
  },

  ceremony: {
    blessing: "॥ శ్రీ మహాగణాధిపతయే నమః ॥",
    occasionTelugu: "శుభ ముహూర్తం",
    weekdayLabel: "Wednesday",
    dateLabel: "November 25th, 2026",
    muhurthamTimeLabel: "Muhurtham at 8:38 PM",
    muhurthamISO: "2026-11-25T20:38:00+05:30",
    inviteLine1: "With the divine blessings of Lord Ganesha and our elders,",
    inviteLine2: "we joyfully invite you and our family to the wedding muhurtham of Maruthi & Vinod. Your presence is the greatest gift — please come, bless the couple, and celebrate with us.",
  },

  events: [
    {
      id: "muhurtham",
      title: "Muhurtham",
      telugu: "ముహూర్తం",
      dateLabel: "Wednesday, 25th November 2026",
      timeLabel: "8:38 PM sharp",
      startISO: "2026-11-25T20:38:00+05:30",
      endISO: "2026-11-25T23:30:00+05:30",
      note: "",
      icon: "fire",
    },
  ],

  venue: {
    name: "Sri Lakshmi AC Convention Hall",
    line1: "Saroornagar, Hyderabad",
    line2: "Telangana – 500035, India",
    address: "Karmanghat Rd, opp. Indra Nagendra Theater, Saroornagar, Hyderabad, Telangana 500035",
    mapsQuery: "Sri Lakshmi AC Convention Hall, Karmanghat Rd, opp. Indra Nagendra Theater, Saroornagar, Hyderabad, Telangana 500035",
    osmEmbed: "https://www.openstreetmap.org/export/embed.html?bbox=78.5115%2C17.3334%2C78.5515%2C17.3574&layer=mapnik&marker=17.3454%2C78.5315",
  },

  images: {
    couple: "./editable/assets/couple.webp",
    garlandTop: "./editable/assets/garland-top.webp",
    mandapFooter: "./editable/assets/mandap-footer.webp",
    ogImage: "./assets/og-image.jpg",
  },

  bgm: {
    src: "./editable/assets/bgm.mp3",
    title: "Seetha Kalyanam",
  },
};
