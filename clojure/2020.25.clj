(use '[io :rename {read-all-lines yummy printI dbg}])

(def inp 
  (->> (yummy)
       (map #(Integer. %))
       ))

(defn step [v sn] (mod (* v sn) 20201227))

(defn find-loop-size [sn pk]
  (loop [v sn ls 1]
    (if (= v pk)
      ls
      (recur (step v sn) (+ 1 ls))
      )))

(defn transform [sn ls]
  (nth (iterate #(step % sn) sn) (- ls 1)))

(->> inp
     ((juxt first #(find-loop-size 7 (second %))))
     (apply transform)
     (dbg)
     )
