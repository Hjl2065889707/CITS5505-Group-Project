export function getDistance(p1, p2) {
  const R = 6371000;
  const toRad = x => x * Math.PI / 180;

  const dLat = toRad(p2.lat - p1.lat);
  const dLng = toRad(p2.lng - p1.lng);

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(p1.lat)) *
    Math.cos(toRad(p2.lat)) *
    Math.sin(dLng / 2) ** 2;

  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function groupPosts(posts) {
  const groups = [];

  posts.forEach(post => {
    let found = false;

    for (let group of groups) {
      const dist = getDistance(post, group[0]);

      if (dist < 50) {
        group.push(post);
        found = true;
        break;
      }
    }

    if (!found) {
      groups.push([post]);
    }
  });

  return groups;
}