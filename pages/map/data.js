// data.js

export const posts = [
  {
    id: "post_001",
    author: {
      userId: "user_101",
      username: "BassHunter99",
      avatarUrl: "https://images.pexels.com/photos/1036622/pexels-photo-1036622.jpeg"
    },
    content: "Great weekend out on the river! The weather was perfect and the fish were biting early in the morning. Best catch of the season so far.",
    photos: [
      "https://images.pexels.com/photos/3220790/pexels-photo-3220790.jpeg"
    ],
    catchDetails: {
      species: "Largemouth Bass",
      weight: "4.5 lbs",
      bait: "Plastic Worm",
      location: {
        name: "Swan River, Perth",
        latitude: -31.95,
        longitude: 115.86
      }
    },
    metrics: {
      likes: 24,
      commentsCount: 5
    },
    createdAt: "2026-03-30T08:30:00Z",
    comments: [
      {
        id: "c1",
        username: "RiverKing",
        text: "Nice catch!",
        createdAt: "2026-03-30T10:00:00Z"
      },
      {
        id: "c2",
        username: "FishPro",
        text: "What bait did you use?",
        createdAt: "2026-03-30T11:00:00Z"
      },
      {
        id: "c3",
        username: "AnglerX",
        text: "🔥🔥🔥",
        createdAt: "2026-03-30T12:00:00Z"
      }]
  },

  {
    id: "post_002",
    author: {
      userId: "user_102",
      username: "OceanExplorer",
      avatarUrl: "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg"
    },
    content: "First time deep sea fishing and it did not disappoint.",
    photos: [
      "https://images.pexels.com/photos/2132007/pexels-photo-2132007.jpeg"
    ],
    catchDetails: {
      species: "Yellowfin Tuna",
      weight: "32 kg",
      bait: "Live Squid",
      location: {
        name: "Rottnest Island Trench",
        latitude: -31.981,
        longitude: 115.82
      }
    },
    metrics: {
      likes: 156,
      commentsCount: 18
    },
    createdAt: "2026-03-31T06:15:00Z"
  },

  {
    id: "post_003",
    author: {
      userId: "user_103",
      username: "QuietAngler",
      avatarUrl: "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg"
    },
    content: "Just a small one today, but the peacefulness of the lake makes up for it.",
    photos: [
      "https://images.pexels.com/photos/17250336/pexels-photo-17250336.jpeg"
    ],
    catchDetails: {
      species: "Rainbow Trout",
      weight: "1.2 lbs",
      bait: "Fly",
      location: {
        name: "Serpentine Dam",
        latitude: -32.4,
        longitude: 116.1
      }
    },
    metrics: {
      likes: 8,
      commentsCount: 1
    },
    createdAt: "2026-03-31T10:45:00Z"
  },

  {
    id: "post_004",
    author: {
        userId: "user_104",
        username: "BridgeCaster",
        avatarUrl: "https://images.pexels.com/photos/91227/pexels-photo-91227.jpeg"
    },
    content: "Tried under Canning Bridge this morning. Water was calm but fish were a bit shy.",
    photos: [
        "https://images.pexels.com/photos/2132007/pexels-photo-2132007.jpeg"
    ],
    catchDetails: {
        species: "Bream",
        weight: "1.1 kg",
        bait: "Soft plastic",
        location: {
        name: "Canning Bridge",
        latitude: -32.0165,
        longitude: 115.8570
        }
    },
    metrics: {
        likes: 12,
        commentsCount: 3
    },
    createdAt: "2026-03-31T06:10:00Z",
    comments: [
        { id: "c1", username: "RiverPro", text: "Nice spot!", createdAt: "" },
        { id: "c2", username: "HookedWA", text: "Try sunset next time", createdAt: "" },
        { id: "c3", username: "AnglerMike", text: "Good effort!", createdAt: "" }
    ]
    },

    {
    id: "post_005",
    author: {
        userId: "user_105",
        username: "NightFisher",
        avatarUrl: "https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg"
    },
    content: "Night fishing near the bridge. Quiet but managed one decent catch.",
    photos: [
        "https://images.pexels.com/photos/3220790/pexels-photo-3220790.jpeg"
    ],
    catchDetails: {
        species: "Flathead",
        weight: "2.3 kg",
        bait: "Live shrimp",
        location: {
        name: "Canning River near bridge",
        latitude: -31.9970,
        longitude: 115.8540
        }
    },
    metrics: {
        likes: 28,
        commentsCount: 5
    },
    createdAt: "2026-03-31T12:20:00Z",
    comments: [
        { id: "c1", username: "FishWA", text: "Nice flathead!", createdAt: "" },
        { id: "c2", username: "CasterX", text: "That’s a solid one", createdAt: "" },
        { id: "c3", username: "RiverKing", text: "🔥🔥🔥", createdAt: "" }
    ]
    },

    {
    id: "post_006",
    author: {
        userId: "user_106",
        username: "KayakHunter",
        avatarUrl: "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg"
    },
    content: "Kayaking past Canning Bridge and spotted a few schools. Good session overall.",
    photos: [
        "https://images.pexels.com/photos/1430677/pexels-photo-1430677.jpeg"
    ],
    catchDetails: {
        species: "Mulloway",
        weight: "6.5 kg",
        bait: "Soft lure",
        location: {
        name: "Canning Bridge waters",
        latitude: -32.0158,
        longitude: 115.8565
        }
    },
    metrics: {
        likes: 64,
        commentsCount: 10
    },
    createdAt: "2026-03-31T08:45:00Z",
    comments: [
        { id: "c1", username: "OceanPro", text: "Huge catch!", createdAt: "" },
        { id: "c2", username: "WAangler", text: "That’s impressive", createdAt: "" },
        { id: "c3", username: "BaitMaster", text: "What lure?", createdAt: "" }
    ]
    },

    {
    id: "post_007",
    author: {
        userId: "user_107",
        username: "WeekendAngler",
        avatarUrl: "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg"
    },
    content: "Busy weekend at Canning Bridge. Lots of people but still worth it.",
    photos: [
        "https://images.pexels.com/photos/17250336/pexels-photo-17250336.jpeg"
    ],
    catchDetails: {
        species: "Herring",
        weight: "0.8 kg",
        bait: "Bread",
        location: {
        name: "Canning Bridge",
        latitude: -32.0162,
        longitude: 115.8573
        }
    },
    metrics: {
        likes: 9,
        commentsCount: 2
    },
    createdAt: "2026-03-31T14:00:00Z",
    comments: [
        { id: "c1", username: "LocalFish", text: "Always crowded there", createdAt: "" },
        { id: "c2", username: "HookedLife", text: "Still fun though!", createdAt: "" }
    ]
    }
];