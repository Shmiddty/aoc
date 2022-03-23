(use '[io :rename {read-all-lines yummy, printI dbg}])
(use '[cartesian :only (enum2d, zone, make-hash-map)])
(use '[util :only (fargo)])

(def inp
  (->> (yummy)
       (map (partial map (partial = \#)))
       (enum2d)
       (filter second)
       (map (partial apply (fargo #(concat % [0]) identity)))
       (make-hash-map)
       ))

(defn isactive [state pt] (get state pt false))

(defn numactive [state pt]
  (->> pt
       (zone)
       (filter (partial not= pt))
       (filter (partial isactive state))
       (count)
       ))

(defn step [state]
  (->> (keys state)
       (mapcat zone)
       (set)
       (filter
         (fn [pt]
           (->> (numactive state pt)
                (#(if (isactive state pt)
                    (or (= 2 %) (= 3 %))
                    (= 3 %)
                    ))
                )))
       (map #(vector % true))
       (make-hash-map)
       ))

(->> inp
     (iterate step)
     (#(nth % 6))
     (keys)
     (count)
     (println)
     )

(->> inp ; pathetic 3D cube-space

     (keys)
     (map #(vector (concat % [0]) true)) ; now in 4D baybeeee
     (make-hash-map)

     (iterate step)
     (#(nth % 6))
     (keys)
     (count)
     (println)
     )

