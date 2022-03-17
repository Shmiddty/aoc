(use '[io :rename {read-all-lines yummy printI printI}])
(use '[enum :only (combinations)])

(def inp
  (->> (yummy)
       (map read-string)
       (apply vector)
       ))

(def N 25)

(defn findsubseq [A ls]
  (->> ls
       (reductions conj [])
       (drop-while #(> A (reduce + %)))
       (first)
       (#(if (= A (reduce + %)) % (findsubseq A (rest ls))))
       ))

(->> inp
     (map-indexed #(vector %1 %2))
     (#(nthrest % N))
     (drop-while
       #(contains?
          (set (map
            (partial reduce +)
            (combinations 2 (subvec inp (- (first %) N) (first %)))
            ))
          (second %)
          ))
     (first)
     (second)
     (printI)
     (#(findsubseq % inp))
     (#(+ (apply min %) (apply max %)))
     (printI)
     )

