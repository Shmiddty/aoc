(use '[io :rename {read-all yummy debug dbg}])
(use '[clojure.string :only (split)])
(use '[clojure.set :only (union, intersection)])

(def inp
  (->> (yummy)
       (#(split % #"\n\n"))
       (map #(split % #"\n"))
       ))

; Part 1
(->> inp
     (map #(->> % (map set) (reduce union)))
     (map count)
     (reduce +)
     (println)
     )

; Part 2
(->> inp
     (map #(->> % (map set) (reduce intersection)))
     (map count)
     (reduce +)
     (println)
     )

