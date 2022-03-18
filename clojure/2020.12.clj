(use '[io :rename {read-all-lines yummy, printI printI}])
(use '[cartesian :only (manhattan, move, turn)])

(def inp
  (->> (yummy)
       (map #(re-matches #"(.)(\d+)" %))
       (map (fn [[_ op v]] [op (read-string v)]))
       ))


(defn step [[pos dir] [op v]]
  (case op
    "N" [(move pos [ 0 -1] v) dir]
    "S" [(move pos [ 0  1] v) dir]
    "E" [(move pos [ 1  0] v) dir]
    "W" [(move pos [-1  0] v) dir]
    "L" [pos (turn dir (* -1 v))]
    "R" [pos (turn dir v)]
    "F" [(move pos dir v) dir]
    ))

(defn step2 [[pos dir] [op v]]
  (case op
    "N" [pos (move dir [ 0 -1] v)]
    "S" [pos (move dir [ 0  1] v)]
    "E" [pos (move dir [ 1  0] v)]
    "W" [pos (move dir [-1  0] v)]
    "L" [pos (turn dir (* -1 v))]
    "R" [pos (turn dir v)]
    "F" [(move pos dir v) dir]
    ))

(->> inp
     ((juxt
        #(->> %
              (apply conj [[[0 0] [1 0]]])
              (reduce step)
              (first)
              (manhattan [0 0])
              (printI)
              )
        #(->> %
              (apply conj [[[0 0] [10 -1]]])
              (reduce step2)
              (first)
              (manhattan [0 0])
              (printI)
              )
        ))
     )

