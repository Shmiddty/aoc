(use '[io :rename {read-all yummy, printI dbg}])
(use '[clojure.string :only (split)])
(use '[util :only (fargo)])
(use '[enum :only (make-hash-map, cross)])

(def inp
  (->> (yummy)
       (#(split % #"\n\n"))
       (apply
         (fargo
           (fn [rules]
             (->> (split rules #"\n")
                  (map (partial re-matches #"(\d+): (\"(([ab]))\"|((\d+ ?)+)\|? ?((\d+ ?)*))"))
                  (map rest)
                  (map (partial take-nth 2))
                  (map (partial filter identity))
                  (map (juxt first (fn [toks] (filter not-empty (map #(filter not-empty (split % #" ")) (rest toks))))))
                  ; I need to come up with a better way of parsing inputs
                  (make-hash-map)
                  ))
           #(split % #"\n")
           ))
       ))

(def rules (first inp))
(def make
  (memoize
    (fn [rule]
      (if (contains? rules rule)
        (mapcat
          (fn [subrule]
            (reduce
              (fn [acc v] (map (partial apply str) (cross acc v)))
              [""]
              (map make subrule)
              ))
          (get rules rule)
          )
        [rule]
        ))))

(def validzero (set (make "0")))
(def messages (second inp))

(->> messages
     (filter (partial contains? validzero))
     (count)
     (println)
     )

; brain is drained. save part 2 for later.
