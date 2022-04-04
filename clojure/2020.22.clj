(use '[io :rename {read-all yummy printI dbg}])
(use '[clojure.string :only (split)])

; this is too verbose.
;(defn combat [[ayy bee]]
;  (loop [A ayy B bee]
;    (if (or (empty? A) (empty? B))
;      (concat A B)
;      (if (> (first A) (first B))
;        (recur (concat (rest A) [(first A) (first B)]) (rest B))
;        (recur (rest A) (concat (rest B) [(first B) (first A)]))
;        ))))

; needing to recombine a and A or b and B at the end is kinda awkward.
;(defn combat [[ayy bee]]
;  (loop [[a & A] ayy [b & B] bee]
;    (if (and a b)
;      (if (> a b)
;        (recur (concat A [a b]) B)
;        (recur A (concat B [b a]))
;        )
;      (if a
;        (concat [a] A)
;        (concat [b] B)
;      ))))

(defn step [[[a & A] [b & B]]]
  (if (> a b)
    [(concat A [a b]) B]
    [A (concat B [b a])]
    ))

; This is nicer.
(defn combat [decks]
  (loop [[A B] decks]
    (if (or (empty? A) (empty? B))
      [A B]
      (recur (step [A B]))
      )))

(def inp
  (as->
    (yummy) x
    (split x #"\n\n")
    (map #(split % #"\n") x)
    (map rest x)
    (map (partial map read-string) x)
    ))

(->>
  inp
  (combat)
  (filter not-empty)
  (first)
  (reverse)
  (concat [0])
  (map-indexed #(* %1 %2))
  (reduce +)
  (println)
  )

(def rstep (memoize (fn [[a & A] [b & B] [Eh Be]]
  (if (> (count Eh) (count Be))
    [(concat A [a b]) B]
    [A (concat B [b a])]
    ))))

(def rcombat (memoize (fn [decks]
  (loop [[A B] decks P #{}]
    (cond
      (or (empty? A) (empty? B)) [A B]
      (contains? P [A B]) [A []]
      (and (<= (first A) (count (rest A))) (<= (first B) (count (rest B))))
        (as-> (rcombat [(rest A) (rest B)]) $ (recur (rstep A B $) (conj P [A B])))
      :else (recur (step [A B]) (conj P [A B]))
      )))))

(->>
  inp
  (rcombat)
  (filter not-empty)
  (first)
  (reverse)
  (concat [0])
  (map-indexed #(* %1 %2))
  (reduce +)
  (println)
  )

