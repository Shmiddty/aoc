(use '[io :rename {read-all-lines yummy, printI printI}])
(use '[enum :only (enumerate)])

(defn pow [a b] (nth (iterate (partial * a) 1) b))

(defn makemask [string] (filter identity
  (map-indexed (fn [i v]
    (case v
       \X false
       \0 #(- (bit-or % (pow 2 i)) (pow 2 i))
       \1 #(bit-or % (pow 2 i))
       ))
    (reverse string)
    )
  ))

(defn applymask [value mask] (reduce #(%2 %1) value mask))

(defn setmasked [[state mask] [reg value]]
  (merge state (hash-map reg (applymask value mask)))
  )

(defn step [[state mask] line]
  (if (= \a (nth line 1))
    [state (makemask (last (re-matches #"mask = (.+)" line)))]
    [(setmasked [state mask] (map read-string (re-seq #"\d+" line))) mask]
    ))

(def inp (yummy))

(->> inp
     (reduce step [{} []])
     (first)
     (vals)
     (reduce +)
     (println)
     )

(defn makemask2 [string] (filter identity
  (map-indexed (fn [i v]
    (case v
       \X false
       \0 identity
       \1 #(bit-or % (pow 2 i))
       ))
    (reverse string)
    )
  ))

(defn applyfloating [value mask]
  (reduce
    (fn [acc i]
      (distinct (concat
        acc
        (map #(bit-or % (pow 2 i)) acc)
        (map #(- (bit-or % (pow 2 i)) (pow 2 i))  acc)
        )))
    [value]
    (map first (filter #(= \X (second %)) (enumerate (reverse mask))))
    ))

(defn setmasked2 [[state mask] [reg value]]
  (apply merge
         state
         (map
           #(hash-map % value)
           (applyfloating (applymask reg (makemask2 mask)) mask)
           ))
  )

(defn step2 [[state mask] line]
  (if (= \a (nth line 1))
    [state (last (re-matches #"mask = (.+)" line))]
    [(setmasked2 [state mask] (map read-string (re-seq #"\d+" line))) mask]
    ))

; Part 2. I suspect there's a better way to do this, but it may still be necessary to generate all of the memory addresses to ensure we're not counting any of them more than once.
; that is, if no addresses collide, then the solution would be something like
; (reduce + (* value (pow 2 (filter #(= \X %) mask))))
; a quick test has shown that the sample problems do have address collisions
(->> inp
     (reduce step2 [{} []])
     (first)
     (vals)
     (reduce +)
     (println)
     )

