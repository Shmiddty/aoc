(use '[io :rename {read-all-lines yummy debug dbg}])

(def inp
  (->> (yummy)
       (map
         #(->> %
               (re-seq #"((^|\d+) ?(\w+ \w+) bags?)")
               (map (partial take-last 2))
               ((fn [v] (vector (second (first v)) (rest v))))
               ; [outer ((num type) (num type))]
               ))
       ))

(defn outerbags [bag]
  (->> (filter
         (fn [v]
           (->> v
                (second)
                (filter #(= bag (second %)))
                (count)
                (#(> % 0))
                ))
          inp)
       (map first)
       (#(apply conj % (mapcat outerbags %)))
       (set)
       ))

(defn countbags [bag]
  (->> inp
       (filter #(= bag (first %)))
       (first) ; there can only be one! (it'd be nice to get the only item with the previous line)
       (second)
       (map #(* (Integer. (first %)) (countbags (second %))))
       (reduce +)
       (+ 1)
       ))

; Part 1
(->> "shiny gold"
     (outerbags)
     (count)
     (println)
     )

; Part 2
(->> "shiny gold"
     (countbags)
     (+ -1) ; we don't want to count the shiny gold back itself
     (println)
     )
