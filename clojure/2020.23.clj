(use '[io :rename {read-all yummy printI dbg}])

(def cups0 (map #(Character/digit % 10) (butlast (yummy))))

(defn move [[A b c d & cups]]
  (as-> cups C
    (if (every? (partial < A) C)
      (split-at (inc (.indexOf C (apply max C))) C)
      (split-at (inc (.indexOf C (apply max (filter (partial > A) C)))) C)
      )
    (apply #(concat %1 [b c d] %2 [A]) C)
    ))

(->>
  cups0
  (iterate move)
  (take 101)
  (last)
  (cycle)
  (drop-while (partial not= 1))
  (next)
  (take (dec (count cups0)))
  (apply str)
  (println)
  )
