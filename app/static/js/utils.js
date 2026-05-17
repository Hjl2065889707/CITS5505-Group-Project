// Haversine distance calculation.
// Returns the approximate distance in metres between two latitude/longitude points.
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

// Grouping logic
// Groups posts that are geographically close together.
// The threshold is in metres and changes depending on map zoom level.
export function groupPosts(posts, threshold = 50) {
  const groups = [];

  posts.forEach(post => {
    let found = false;

    // Compare this post with the first post in each existing group.
    // If it is close enough, add it to that group.
    for (let group of groups) {
      const dist = getDistance(
        {
          lat: post.latitude,
          lng: post.longitude
        },
        {
          lat: group[0].latitude,
          lng: group[0].longitude
        }
      );

      if (dist < threshold) {
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