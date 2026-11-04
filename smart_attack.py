from sage.all import *

# helper function for finding lift point

def lift_points(Eq, x, y):
    
    lift_Eq = Eq.lift_x(x, all=True)

    for i in range(len(lift_Eq)):
        if lift_Eq[i][1].residue() == y:
            return lift_Eq[i]
    raise ValueError("No lift found.")

def smart_attack(E, P, Q):

    # extract values from the defined elliptic curve

    p = ZZ(E.base_field().order())
    a1 = ZZ(E.a_invariants()[0])
    a2 = ZZ(E.a_invariants()[1])
    a3 = ZZ(E.a_invariants()[2])
    a4 = ZZ(E.a_invariants()[3])
    a6 = ZZ(E.a_invariants()[4])

    # cardinality check
    
    if E.order() != p:
        raise ValueError("Curve is not anomalous; Smart's attack does not apply.")
    
    # define coordinates as integers
    
    P_x = ZZ(P[0])
    P_y = ZZ(P[1])
    Q_x = ZZ(Q[0])
    Q_y = ZZ(Q[1])

    # create elliptic curve over p-adic field Q_p

    Qp = pAdicField(p, 8)
    Eq = EllipticCurve(Qp, [a1, a2, a3, a4, a6])

    # lift the points for P and Q over the defined elliptic curve

    Pq = lift_points(Eq, P_x, P_y)

    Qq = lift_points(Eq, Q_x, Q_y)

    # multiply by p and compute ψ = −x/y

    pq = (p*Pq).xy()
    qq = (p*Qq).xy()

    logpq = -pq[0]/pq[1]
    logqq = -qq[0]/qq[1]

    if logpq.valuation() != 1:
        raise ValueError("ψ(pP) divisible by p²: canonical lift, re-lift with different coefficients.")
    
    m = (logqq/logpq).residue()

    # recover the secret
    
    return m