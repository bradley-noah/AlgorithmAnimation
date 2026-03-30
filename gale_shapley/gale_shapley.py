import random


def gale_shapley(proposer_prefs, receiver_prefs):
    events = []

    proposers = list(proposer_prefs.keys())
    receivers = list(receiver_prefs.keys())

    if len(proposers) != len(receivers):
        raise ValueError("Numbers of proposers and receivers must match")

    receiver_set = set(receivers)
    proposer_set = set(proposers)

    for proposer in proposers:
        prefs = proposer_prefs[proposer]
        if len(prefs) != len(receivers) or set(prefs) != receiver_set:
            raise ValueError(f"Invalid preference list for proposer {proposer}")

    for receiver in receivers:
        prefs = receiver_prefs[receiver]
        if len(prefs) != len(proposers) or set(prefs) != proposer_set:
            raise ValueError(f"Invalid preference list for receiver {receiver}")

    # Precompute receiver ranking for O(1) preference comparison.
    rank = {
        receiver: {proposer: i for i, proposer in enumerate(receiver_prefs[receiver])}
        for receiver in receivers
    }

    free = proposers[:]
    next_choice_idx = {p: 0 for p in proposers}
    engaged_to = {r: None for r in receivers}  # receiver -> proposer

    while free:
        proposer = free.pop(0)

        if next_choice_idx[proposer] >= len(proposer_prefs[proposer]):
            continue

        receiver = proposer_prefs[proposer][next_choice_idx[proposer]]
        next_choice_idx[proposer] += 1

        current = engaged_to[receiver]

        events.append(
            {
                "type": "propose",
                "proposer": proposer,
                "receiver": receiver,
                "current": current,
            }
        )

        if current is None:
            engaged_to[receiver] = proposer
            events.append(
                {
                    "type": "accept",
                    "proposer": proposer,
                    "receiver": receiver,
                    "replaced": None,
                }
            )
            continue

        if rank[receiver][proposer] < rank[receiver][current]:
            engaged_to[receiver] = proposer
            free.append(current)
            events.append(
                {
                    "type": "accept",
                    "proposer": proposer,
                    "receiver": receiver,
                    "replaced": current,
                }
            )
            events.append(
                {
                    "type": "reject",
                    "proposer": current,
                    "receiver": receiver,
                    "reason": "replaced",
                }
            )
        else:
            free.append(proposer)
            events.append(
                {
                    "type": "reject",
                    "proposer": proposer,
                    "receiver": receiver,
                    "reason": "prefers_current",
                }
            )

    final = {proposer: receiver for receiver, proposer in engaged_to.items() if proposer is not None}
    events.append({"type": "done", "matching": final.copy()})

    return events, final


def make_random_scenario(n=4):
    if n <= 0:
        raise ValueError("n must be positive")

    proposers = [f"M{i}" for i in range(1, n + 1)]
    receivers = [f"W{i}" for i in range(1, n + 1)]

    proposer_prefs = {}
    for proposer in proposers:
        prefs = receivers[:]
        random.shuffle(prefs)
        proposer_prefs[proposer] = prefs

    receiver_prefs = {}
    for receiver in receivers:
        prefs = proposers[:]
        random.shuffle(prefs)
        receiver_prefs[receiver] = prefs

    return proposer_prefs, receiver_prefs


if __name__ == "__main__":
    p_prefs, r_prefs = make_random_scenario(4)
    trace, matching = gale_shapley(p_prefs, r_prefs)

    print("Proposer preferences:")
    for proposer, prefs in p_prefs.items():
        print(f"  {proposer}: {prefs}")

    print("\nReceiver preferences:")
    for receiver, prefs in r_prefs.items():
        print(f"  {receiver}: {prefs}")

    print("\nStable matching:")
    for proposer in sorted(matching):
        print(f"  {proposer} -> {matching[proposer]}")

    print(f"\nEvents recorded: {len(trace)}")
