from typing import List, Tuple, Dict, Any
from rapidfuzz import fuzz

from api.social_manager.models import social_model


class CrossPlatformMapper:

    _instance = None
    _cards: List[social_model] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cards = []
        return cls._instance

    def add_card(self, card: social_model) -> None:
        self._cards.append(card)

    def get_all_cards(self) -> List[social_model]:
        return self._cards

    def get_all_cards_dict(self) -> List[Dict]:
        return [card.model_dump() for card in self._cards]

    def clear_cards(self) -> None:
        self._cards = []

    @staticmethod
    def _platform_key(platform) -> str:
        if isinstance(platform, list):
            return ",".join(str(item) for item in platform)
        return str(platform)

    def get_summary(self) -> Dict[str, Any]:
        if not self._cards:
            return {"total_cards": 0, "cards": []}

        cards_summary = []
        for card in self._cards:
            card_data = {
                "platform": card.m_platform,
                "username": card.m_username,
                "real_name": card.m_real_name,
                "network": card.m_network,
                "bio": card.m_bio,
                "total_posts": card.m_total_posts,
                "total_followers": card.m_total_followers,
                "total_following": card.m_total_following,
                "weblinks": card.m_weblink,
                "content_type": card.m_content_type,
                "followers_count": len(card.m_followers) if card.m_followers else 0,
                "following_count": len(card.m_following) if card.m_following else 0,
                "mutual_count": len(card.m_mutual_usernames) if card.m_mutual_usernames else 0,
                "followers": card.m_followers or [],
                "following": card.m_following or [],
                "mutual_usernames": card.m_mutual_usernames or [],
                "commenters": card.m_commenters or []
            }
            cards_summary.append(card_data)

        return {
            "total_cards": len(self._cards),
            "cards": cards_summary
        }

    def compare_following_across_platforms(self, threshold: int = 70) -> Dict[str, Any]:
        platform_following = {
            self._platform_key(card.m_platform): list(set(card.m_following))
            for card in self._cards
            if card.m_following
        }

        if len(platform_following) < 2:
            return {"status": "insufficient_data", "message": "Need at least 2 platforms with following data"}

        platforms = list(platform_following.keys())
        comparisons = []

        for i in range(len(platforms)):
            for j in range(i + 1, len(platforms)):
                p1, p2 = platforms[i], platforms[j]
                list1 = platform_following[p1]
                list2 = platform_following[p2]

                exact_matches = sorted(set(list1) & set(list2))

                similar_matches = []
                for u1 in list1:
                    for u2 in list2:
                        if u1 == u2:
                            continue
                        score = fuzz.ratio(u1.lower(), u2.lower())
                        if score >= threshold:
                            similar_matches.append({
                                "username_1": u1,
                                "username_2": u2,
                                "similarity": score
                            })

                only_p1 = sorted(set(list1) - set(list2))
                only_p2 = sorted(set(list2) - set(list1))

                comparisons.append({
                    "platform_1": p1,
                    "platform_2": p2,
                    "exact_matches": exact_matches,
                    "exact_matches_count": len(exact_matches),
                    "similar_matches": similar_matches,
                    "similar_matches_count": len(similar_matches),
                    f"only_on_{p1}": only_p1,
                    f"only_on_{p2}": only_p2
                })

        return {
            "status": "success",
            "threshold": threshold,
            "comparisons": comparisons
        }

    def group_following_across_all_platforms(self, threshold: int = 70) -> Dict[str, Any]:
        users: List[Tuple[str, str]] = []
        for card in self._cards:
            if card.m_following:
                for username in card.m_following:
                    users.append((self._platform_key(card.m_platform), username))

        if not users:
            return {"status": "no_data", "identity_groups": []}

        groups: List[List[Tuple[str, str]]] = []

        for platform, username in users:
            matched = False
            for group in groups:
                if any(fuzz.ratio(username, existing_username) >= threshold
                       for _, existing_username in group):
                    group.append((platform, username))
                    matched = True
                    break
            if not matched:
                groups.append([(platform, username)])

        meaningful_groups = [g for g in groups if len(g) > 1]
        identity_groups = []

        for idx, group in enumerate(meaningful_groups, 1):
            group_data = {
                "group_id": idx,
                "members": []
            }
            for platform, username in sorted(group):
                scores = [
                    fuzz.ratio(username, other)
                    for _, other in group
                    if other != username
                ]
                confidence = max(scores) if scores else 100
                group_data["members"].append({
                    "platform": platform,
                    "username": username,
                    "confidence": confidence
                })
            identity_groups.append(group_data)

        return {
            "status": "success",
            "threshold": threshold,
            "total_groups": len(identity_groups),
            "identity_groups": identity_groups
        }

    def analyze_cross_platform_influence(self, threshold: int = 70) -> Dict[str, Any]:
        user_profiles: Dict[str, Dict] = {}

        for card in self._cards:
            platform = self._platform_key(card.m_platform)
            all_connections = []

            if card.m_followers:
                for user in card.m_followers:
                    all_connections.append((user, "follower", platform))

            if card.m_following:
                for user in card.m_following:
                    all_connections.append((user, "following", platform))

            if card.m_mutual_usernames:
                for user in card.m_mutual_usernames:
                    all_connections.append((user, "mutual", platform))

            for username, conn_type, plat in all_connections:
                norm_username = username.lower().strip()
                matched_key = None

                for existing_key in user_profiles.keys():
                    if fuzz.ratio(norm_username, existing_key) >= threshold:
                        matched_key = existing_key
                        break

                if not matched_key:
                    matched_key = norm_username
                    user_profiles[matched_key] = {
                        "original_names": set(),
                        "platforms": set(),
                        "connection_types": set(),
                        "follower_count": 0,
                        "following_count": 0,
                        "mutual_count": 0,
                        "platform_details": {}
                    }

                profile = user_profiles[matched_key]
                profile["original_names"].add(username)
                profile["platforms"].add(plat)
                profile["connection_types"].add(conn_type)

                if conn_type == "follower":
                    profile["follower_count"] += 1
                elif conn_type == "following":
                    profile["following_count"] += 1
                elif conn_type == "mutual":
                    profile["mutual_count"] += 1

                profile.setdefault("platform_details", {}).setdefault(plat, []).append(conn_type)

        if not user_profiles:
            return {"status": "no_data", "influencers": [], "bridge_users": [], "statistics": {}}

        scored_users = []

        for username, profile in user_profiles.items():
            platform_diversity = len(profile["platforms"])
            connection_diversity = len(profile["connection_types"])

            network_score = (
                profile["follower_count"] * 1.5 +
                profile["mutual_count"] * 2.0 +
                profile["following_count"] * 0.5
            )

            influence_score = (
                platform_diversity * 10 +
                connection_diversity * 5 +
                network_score
            )

            scored_users.append({
                "username": username,
                "profile": profile,
                "score": influence_score
            })

        scored_users.sort(key=lambda x: x["score"], reverse=True)

        top_influencers = []
        for user_data in scored_users[:10]:
            profile = user_data["profile"]
            platform_breakdown = {}
            for plat, types in profile["platform_details"].items():
                platform_breakdown[plat] = list(set(types))

            top_influencers.append({
                "username_variations": sorted(profile["original_names"]),
                "influence_score": round(user_data["score"], 1),
                "platforms": sorted(profile["platforms"]),
                "connection_types": sorted(profile["connection_types"]),
                "follower_count": profile["follower_count"],
                "following_count": profile["following_count"],
                "mutual_count": profile["mutual_count"],
                "platform_breakdown": platform_breakdown
            })

        bridge_users = []
        multi_platform_users = [u for u in scored_users if len(u["profile"]["platforms"]) >= 2]

        for user_data in multi_platform_users[:15]:
            profile = user_data["profile"]
            bridge_users.append({
                "username_variations": sorted(profile["original_names"]),
                "platforms": sorted(profile["platforms"]),
                "connection_types": sorted(profile["connection_types"])
            })

        total_users = len(user_profiles)
        multi_platform_count = len([u for u in user_profiles.values() if len(u["platforms"]) > 1])
        avg_platforms = sum(len(u["platforms"]) for u in user_profiles.values()) / total_users if total_users > 0 else 0

        conn_type_dist = {}
        for profile in user_profiles.values():
            for conn_type in profile["connection_types"]:
                conn_type_dist[conn_type] = conn_type_dist.get(conn_type, 0) + 1

        statistics = {
            "total_unique_users": total_users,
            "multi_platform_users": multi_platform_count,
            "multi_platform_percentage": round(multi_platform_count / total_users * 100, 1) if total_users > 0 else 0,
            "average_platforms_per_user": round(avg_platforms, 2),
            "connection_type_distribution": conn_type_dist
        }

        return {
            "status": "success",
            "threshold": threshold,
            "top_influencers": top_influencers,
            "bridge_users": bridge_users,
            "statistics": statistics
        }

    def get_full_analysis(self, threshold: int = 70) -> Dict[str, Any]:
        comparison = self.compare_following_across_platforms(threshold)
        identity = self.group_following_across_all_platforms(threshold)
        influence = self.analyze_cross_platform_influence(threshold)

        result = {
            "platforms_analyzed": len(self._cards),
            "threshold": threshold,
            "cross_platform_matches": [],
            "platform_comparison": [],
            "identity_groups": [],
            "bridge_users": influence.get("bridge_users", []),
            "top_influencers": influence.get("top_influencers", [])[:5],
            "statistics": influence.get("statistics", {})
        }

        if comparison.get("status") == "success":
            for comp in comparison.get("comparisons", []):
                platform_comp = {
                    "platforms": [comp["platform_1"], comp["platform_2"]],
                    "exact_matches": comp.get("exact_matches", []),
                    "similar_matches": comp.get("similar_matches", []),
                    f"only_on_{comp['platform_1']}": comp.get(f"only_on_{comp['platform_1']}", []),
                    f"only_on_{comp['platform_2']}": comp.get(f"only_on_{comp['platform_2']}", [])
                }
                result["platform_comparison"].append(platform_comp)
                
                if comp.get("exact_matches") or comp.get("similar_matches"):
                    result["cross_platform_matches"].append({
                        "platforms": [comp["platform_1"], comp["platform_2"]],
                        "exact_matches": comp.get("exact_matches", []),
                        "similar_matches": comp.get("similar_matches", [])
                    })

        if identity.get("status") == "success":
            result["identity_groups"] = identity.get("identity_groups", [])

        return result


cross_platform_mapper = CrossPlatformMapper()
