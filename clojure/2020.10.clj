(use '[io :rename {read-all-lines yummy, printI printI}])
(use '[enum :only (has)])

(def inp (map read-string (yummy)))

; mebbe shud memo
; it wasn't factorial at all!
(defn fac [n] (if (< n 2) n (* n (fac (- n 1)))))
(defn tri [n] (/ (* n (+ n 1)) 2))

; I should move these somewhere
(def sum (partial reduce +))
(def prod (partial reduce *))

(->> inp
     (#(apply conj [0] (+ 3 (apply max %)) %))
     (sort)
     (reverse)
     (partition 2 1)
     (map (partial reduce -))
     ((juxt
        (fn [v]
          (->> v
               (group-by identity)
               (#(* (count (get % 3)) (count (get % 1))))
               (println)
               ))
        (fn [v]
          (->> v
               (partition-by identity)
               (filter (partial has 1))
               (map count)
               ;(map #(+ 1 (tri (- % 1))))
               ; ^ may be fewer operations but the below seems more clear:
               (map #(- % 1))
               (map tri)
               (map #(+ % 1))
               (prod)
               (println)
               ))
        ))
     )
